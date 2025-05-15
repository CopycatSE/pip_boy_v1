#!/usr/bin/env python3
"""
CLI application for Bunker Radio using Textual.
Implements MVP pattern: BunkerPresenter handles logic, BunkerCLI functions as the View.
"""
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical, Horizontal

from dependencies import register_dependencies
from .presenter import BunkerPresenter
from .widgets import OutputWidget, StatusWidget, InputWidget, MenuOverlay

class BunkerCLI(App):
    CSS_PATH = "theme.css"
    BINDINGS = [
        ("s", "start", "Start"),
        ("c", "copy", "Copy"),
        ("q", "exit", "Exit"),
        ("m", "toggle_menu", "Menu"),
    ]

    def compose(self) -> ComposeResult:
        self.status_widget = StatusWidget(id="status")
        self.output_widget = OutputWidget(id="output")
        self.input_widget = InputWidget(id="input")
        with Vertical(id="layout"):
            yield Horizontal(
                Button("☢ Start", id="start"),
                Button("Copy", id="copy"),
                Button("Exit", id="exit"),
                id="menu_bar",
            )
            yield self.status_widget
            yield self.output_widget
            yield self.input_widget

    def on_mount(self):
        self.container = register_dependencies()
        self.presenter = BunkerPresenter(self, self.container)
        self.status_widget.styles.height = 3
        self.output_widget.styles.height = "1fr"
        self.input_widget.styles.height = 3
        self.menu_overlay = MenuOverlay()
        self.mount(self.menu_overlay)

    async def action_start(self) -> None:
        self.show_loading()
        self.call_later(self.output_widget.refresh)
        self.call_later(lambda: self.run_worker(self.presenter.start))

    async def action_copy(self) -> None:
        self.presenter.copy()

    async def action_exit(self) -> None:
        self.exit()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "start":
            await self.action_start()
        elif btn_id == "copy":
            await self.action_copy()
        elif btn_id == "exit":
            await self.action_exit()
        elif btn_id == "close":
            if self.menu_overlay is not None:
                await self.menu_overlay.remove()

    async def action_toggle_menu(self) -> None:
        if self.menu_overlay.parent is None:
            await self.mount(self.menu_overlay)

    async def display_response(self, response: str) -> None:
        await self.output_widget.display_animated_output(response)

    def get_response(self) -> str:
        return self.output_widget.response

    def refresh_view(self) -> None:
        self.refresh()

    def set_status(self, text: str) -> None:
        self.status_widget.set_status(text)

    def show_loading(self) -> None:
        self.output_widget.show_loading()

if __name__ == "__main__":
    BunkerCLI().run()