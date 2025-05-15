import asyncio
import pyperclip
from pyperclip import PyperclipException
from core.logic import run_bunker_sequence

class BunkerPresenter:
    def __init__(self, view, container):
        self.view = view
        self.container = container

    async def start(self):
        self.view.set_status("Loading")
        self.view.show_loading()
        self.view.refresh_view()
        await asyncio.sleep(0.1)
        try:
            _, response = await run_bunker_sequence(self.container)
            await self.view.display_response(response)
            self.view.set_status("Ready")
        except Exception as e:
            await self.view.display_response(f"Error: {e}")
            self.view.set_status(" Error")

    def copy(self):
        try:
            pyperclip.copy(self.view.get_response())
            self.view.set_status("Copied to clipboard!")
        except PyperclipException as e:
            self.view.set_status("Copy failed")
            # Notify view of copy error asynchronously
            asyncio.create_task(self.view.display_response(f"Copy error: {e}"))
