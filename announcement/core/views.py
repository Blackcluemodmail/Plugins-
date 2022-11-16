from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union, TYPE_CHECKING

import discord
from discord import ButtonStyle, Interaction, TextStyle, ui
from discord.ext import commands
from discord.utils import MISSING

from .models import AnnouncementType


if TYPE_CHECKING:
    from ..announcement import Announcement as AnnouncementCog
    from .models import AnnouncementModel

    ButtonCallbackT = Callable[[Union[Interaction, Any]], Awaitable]


_max_embed_length = 6000
_short_length = 256
_long_length = 4000
type_select_maps = [
    {
        "label": "Plain",
        "emoji": None,
        "description": "Plain text announcement.",
    },
    {
        "label": "Embed",
        "emoji": None,
        "description": "Embedded announcement. Image and thumbnail image are alose supported.",
    },
]
mention_select_maps = [
    {"label": "@here", "description": "Mention @here."},
    {"label": "@everyone", "description": "Mention @everyone."},
    {"label": "Others", "description": "Mention users or roles."},
]


class TextInput(ui.TextInput):
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        super().__init__(**kwargs)


class Modal(ui.Modal):

    children: List[TextInput]

    def __init__(self, view: AnnouncementView, options: Dict[str, Any]):
        super().__init__(title="Announcement")
        self.view = view
        self.view.modals.append(self)
        for key, value in options.items():
            self.add_item(TextInput(key, **value))

    async def on_submit(self, interaction: Interaction) -> None:
        for child in self.children:
            self.view.inputs[child.name]["default"] = child.value

        await interaction.response.defer()
        self.stop()
        await self.view.on_modal_submit(interaction)


class SelectMenu(ui.Select):
    def __init__(self, *, options: List[discord.SelectOption], callback: Callable[..., Awaitable], **kwargs):
        super().__init__(
            options=options,
            **kwargs,
        )
        self.followup_callback: Callable[..., Awaitable] = callback

    async def callback(self, interaction: Interaction) -> None:
        assert self.view is not None
        await self.followup_callback(interaction, self)


class ChannelSelect(ui.ChannelSelect):
    """
    Channel select. Here, we just want to override the callback.
    """

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        assert self.view is not None
        value = self.values[0]
        self.placeholder = value.name
        channel = value.resolve() or await value.fetch()
        self.view.announcement.channel = channel
        await self.view.update_view()


class MentionableSelect(ui.MentionableSelect):
    """
    Mentionable select. Here, we just want to override the callback.
    """

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        assert self.view is not None
        if self.values:
            self.view.announcement.content = ", ".join(v.mention for v in self.values)
        else:
            self.view.announcement.content = MISSING


class Button(ui.Button["AnnouncementView"]):
    def __init__(
        self,
        *,
        label: str,
        style: ButtonStyle = ButtonStyle.blurple,
        callback: ButtonCallbackT = MISSING,
        **kwargs,
    ):
        super().__init__(label=label, style=style, **kwargs)
        self.followup_callback: ButtonCallbackT = callback

    async def callback(self, interaction: Interaction) -> None:
        assert self.view is not None
        await self.followup_callback(interaction, self)


class AnnouncementView(ui.View):
    """
    Represents the AnnouncementView class. The announcement creation panel and sessions
    will be handled from here.
    """

    children: List[Button]

    def __init__(
        self,
        ctx: commands.Context,
        announcement: AnnouncementModel,
        *,
        input_sessions: List[Tuple[str]],
        timeout: float = 600.0,
    ):
        super().__init__(timeout=timeout)
        self.ctx: commands.Context = ctx
        self.cog: AnnouncementCog = ctx.cog
        self.user: discord.Member = ctx.author
        self.announcement: AnnouncementModel = announcement
        self.input_sessions: List[Tuple[str]] = input_sessions
        self.index: int = 0
        self.message: discord.Message = MISSING
        self.confirm: Optional[bool] = None
        self._underlying_modals: List[Modal] = []

        self.embed_data: Dict[str, Any] = {
            "description": {
                "label": "Announcement",
                "style": TextStyle.long,
                "max_length": _long_length,
            },
            "thumbnail_url": {
                "label": "Thumbnail URL",
                "required": False,
                "max_length": _short_length,
            },
            "image_url": {
                "label": "Image URL",
                "required": False,
                "max_length": _short_length,
            },
            "color": {
                "label": "Embed color",
                "required": False,
                "max_length": 20,
            },
        }
        self.inputs: Dict[str, Any] = {}
        self.mentionable_select: MentionableSelect = MISSING

    @property
    def modals(self) -> List[Modal]:
        return self._underlying_modals

    @property
    def session_description(self) -> None:
        return self.input_sessions[self.index][1]

    def _add_menu(self) -> None:
        options = []
        for type_option in type_select_maps:
            option = discord.SelectOption(
                label=type_option["label"],
                emoji=type_option["emoji"],
                description=type_option["description"],
                value=type_option["label"].lower(),
            )
            options.append(option)

        type_select = SelectMenu(
            options=options,
            callback=self._type_select_callback,
            placeholder="Choose a type",
            row=0,
        )
        self.add_item(type_select)

    def generate_buttons(self, *, post: bool = False, confirmation: bool = False) -> None:
        if confirmation:
            buttons = {
                "yes": (ButtonStyle.green, self._action_confirmation),
                "no": (ButtonStyle.red, self._action_confirmation),
            }
        else:
            if post:
                first_elem = {"post": (ButtonStyle.green, self._action_post)}
            else:
                first_elem = {"next": (ButtonStyle.blurple, self._action_next)}
            buttons: Dict[str, Any] = {
                **first_elem,
                "edit": (ButtonStyle.grey, self._action_edit),
                "preview": (ButtonStyle.grey, self._action_preview),
                "cancel": (ButtonStyle.red, self._action_cancel),
            }
        for label, item in buttons.items():
            self.add_item(Button(label=label.title(), style=item[0], callback=item[1]))

    def refresh(self) -> None:
        for child in self.children:
            if not isinstance(child, Button):
                continue
            if child.label.lower() == "cancel":
                continue
            if not self.announcement.type:
                child.disabled = True
                continue
            if child.label.lower() in ("post", "preview", "next"):
                child.disabled = not self.announcement.ready
            elif child.label.lower() == "edit":
                child.disabled = self.input_sessions[self.index][0] not in ("embed", "plain")
            else:
                child.disabled = False

    async def create_base(self) -> None:
        """
        Create a base message and attach this view's components to it.
        """
        if self.message is not MISSING:
            raise RuntimeError("The base message already exists.")
        self._add_menu()
        self.generate_buttons()
        self.refresh()
        embed = discord.Embed(
            title="Announcement Creation Panel",
            description=self.session_description,
            color=self.ctx.bot.main_color,
        )
        self.message = await self.ctx.send(embed=embed, view=self)

    def _populate_base_inputs(self, type_: AnnouncementType) -> None:
        if type_ == AnnouncementType.EMBED:
            self.inputs.update(**self.embed_data)
        else:
            content = {
                "label": "Content",
                "default": None,
                "style": TextStyle.long,
                "max_length": _long_length,
            }
            self.inputs["content"] = content

    def _resolve_unused_sessions(self) -> None:
        for session in self.input_sessions:
            stype = session[0]
            if self.announcement.type == AnnouncementType.EMBED:
                if stype == "plain":
                    self.input_sessions.remove(session)
            elif self.announcement.type == AnnouncementType.PLAIN:
                if stype in ("embed", "mention"):
                    self.input_sessions.remove(session)
            else:
                raise TypeError(f"Invalid type of announcement, `{self.announcement.type}`.")

    async def _type_select_callback(self, interaction: Interaction, select: SelectMenu) -> None:
        # interaction will be deferred in _action_next
        value = select.values[0]
        select.placeholder = value.title()
        select.disabled = True
        self.announcement.type = AnnouncementType.from_value(value)
        self._resolve_unused_sessions()
        await self._action_next(interaction, None)

    async def _mention_select_callback(self, interaction: Interaction, select: SelectMenu) -> None:
        await interaction.response.defer()
        value = select.values[0]
        select.placeholder = value
        if value in ("@here", "@everyone"):
            self.mentionable_select.disabled = True
            self.announcement.content = value
        else:
            self.mentionable_select.disabled = False
            self.announcement.content = MISSING
        await self.update_view()

    async def _action_post(self, *args: Tuple[Interaction, Button]) -> None:
        interaction, _ = args
        await interaction.response.defer()
        self.clear_items()
        self.announcement.event.set()

    async def _action_next(self, *args: Tuple[Interaction, Optional[Button]]) -> None:
        interaction, _ = args
        await interaction.response.defer()
        self.index += 1
        current = self.input_sessions[self.index][0]
        self.inputs.clear()
        self.clear_items()
        post = False
        if current in ("embed", "plain"):
            self._populate_base_inputs(self.announcement.type)
            description = f"__**{current.title()}:**__\n"
        elif current == "mention":
            options = []
            for ms in mention_select_maps:
                options.append(discord.SelectOption(**ms))
            mention_select = SelectMenu(
                options=options,
                callback=self._mention_select_callback,
                placeholder="Select mention",
                row=0,
            )
            self.add_item(mention_select)
            self.mentionable_select = MentionableSelect(
                min_values=0,
                max_values=25,
                placeholder="Other mentions",
                disabled=True,
                row=1,
            )
            self.add_item(self.mentionable_select)
            description = "__**Select mentions:**__\n"
        elif current == "channel":
            post = True
            channel_select = ChannelSelect(
                channel_types=[discord.ChannelType.news, discord.ChannelType.text],
                placeholder="Select a channel",
                row=0,
            )
            self.add_item(channel_select)
            description = "__**Select a channel:**__\n"
        else:
            raise ValueError(f"Invalid session in `_action_next`: `{current}`.")
        description += f"{self.session_description}\n"
        embed = self.message.embeds[0]
        embed.description = description
        self.generate_buttons(post=post)
        await self.update_view()

    async def _action_edit(self, *args: Tuple[Interaction, Button]) -> None:
        interaction, _ = args
        modal = Modal(self, self.inputs)
        await interaction.response.send_modal(modal)
        await modal.wait()

    async def _action_preview(self, *args: Tuple[Interaction, Button]) -> None:
        interaction, _ = args
        try:
            await interaction.response.send_message(ephemeral=True, **self.announcement.send_params())
        except discord.HTTPException as exc:
            error = f"**Error:**\n```py\n{type(exc).__name__}: {str(exc)}\n```"
            await interaction.response.send_message(error, ephemeral=True)

    async def _action_cancel(self, *args: Tuple[Interaction, Button]) -> None:
        interaction, _ = args
        self.announcement.cancel()
        self.disable_and_stop()
        await interaction.response.edit_message(view=self)

    async def _action_confirmation(self, interaction: Interaction, button: Button) -> None:
        await interaction.response.defer()
        value = button.label.lower()
        self.confirm = value == "yes"
        self.disable_and_stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.user.id == interaction.user.id:
            return True

        await interaction.followup.send(
            "This panel cannot be controlled by you!",
            ephemeral=True,
        )
        return False

    async def on_modal_submit(self, interaction: Interaction) -> None:
        errors = []
        if self.announcement.type == AnnouncementType.EMBED:
            elems = [
                "description",
                "thumbnail_url",
                "image_url",
                "color",
            ]
            kwargs = {elem: self.inputs[elem].get("default") for elem in elems}
            try:
                self.announcement.create_embed(**kwargs)
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: {str(exc)}")
        else:
            self.announcement.content = self.inputs["content"].get("default")

        if errors:
            self.announcement.ready = False
            content = "\n".join(f"{n}. {error}" for n, error in enumerate(errors, start=1))
            embed = discord.Embed(
                title="__Errors__",
                color=self.ctx.bot.error_color,
                description=content,
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            self.announcement.ready = True
        await self.update_view()

    async def wait(self, *, input_event: bool = False) -> None:
        if self.message is MISSING:
            raise RuntimeError("The base message has not been created yet.")

        if input_event:
            await self.announcement.wait()
        else:
            await super().wait()

    async def update_view(self) -> None:
        """
        Refresh the components and update the view.
        """
        self.refresh()
        await self.message.edit(embed=self.message.embeds[0], view=self)

    def disable_and_stop(self) -> None:
        for child in self.children:
            child.disabled = True
        for modal in self.modals:
            if modal.is_dispatching() or not modal.is_finished():
                modal.stop()
        if not self.is_finished():
            self.stop()

    async def on_timeout(self) -> None:
        self.announcement.cancel()
        self.disable_and_stop()
        await self.message.edit(view=self)
