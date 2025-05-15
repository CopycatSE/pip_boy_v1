from textual.widgets import Button
from textual.containers import Vertical
from textual.widgets import Input, Button
from textual.containers import Horizontal
from textual.message import Message
# Widgets for the CLI UI, including output and status panels with animation and panel formatting
from textual.widgets import Static
from rich.text import Text
import asyncio
from rich.panel import Panel
from rich.align import Align


# OutputWidget handles animated display of text output in the main content area
class OutputWidget(Static):
    # Initialize the widget and set up internal state
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headlines = ""
        self.response = ""
        self.loading = False
        self.can_focus = True
        self.scrollable = True
        self.display_buffer = ""

    # Display a "Loading" message immediately and refresh the widget
    def show_loading(self):
        self.loading = True
        self.display_buffer = ""
        self.response = ""
        self.refresh(layout=True)
        self.update(self.render())

    # Animate text output character-by-character for dramatic effect
    async def display_animated_output(self, text: str, delay: float = 0.002) -> None:
        self.response = text
        self.display_buffer = ""
        self.loading = False
        for char in text:
            self.display_buffer += char + "⣿"
            self.update(self.render())
            await asyncio.sleep(delay)
            self.display_buffer = self.display_buffer[:-1]
        self.display_buffer = ""
        self.update(self.render())

    # Reset the output content and clear the display
    def clear(self) -> None:
  
        self.response = ""
        self.display_buffer = ""
        self.update(self.render())

    # Render the current output content as a Rich Text object
    def render(self) -> Panel:
        """
        Render the output area inside a styled panel.
        Displays either the animated display_buffer or the current response.
        """
        content_text = self.display_buffer if self.display_buffer else self.response

        # Use a different visual while loading
        text_style = "italic #888888" if self.loading else "bold #c0c0c0"
        border_style = "dim #666666" if self.loading else "bold #5f5fa0"
        title = " Loading..." if self.loading else "BUNKER RADIO"

        body = Text(content_text, justify="left", style=text_style)

        return Panel(
            body,
            title=title,
            title_align="left",
            border_style=border_style,
            padding=(0, 1),
        )

# StatusWidget shows current status in a bordered panel with a title
class StatusWidget(Static):
    # Set up initial status value
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status = "Stand by"

    # Update the status text and trigger a re-render
    def set_status(self, text: str):
        self.status = text
        self.update(self.render())

    # Render the status line inside a titled panel
    # The title appears centered on the panel border
    def render(self) -> Panel:
        bar_text = Text(self._build_status_text(), style="bold")
        return Panel(
            Align.center(bar_text),
            title="STATUS",
            title_align="left",
        )

    def _build_status_text(self) -> str:
        return f"╰──────── {self.status} ──────────╯"




# InputWidget allows user to type text and submit it, wrapped in a styled Panel-like container
from textual.containers import Container

class InputWidget(Static):
    class Submitted(Message):
        def __init__(self, sender, content: str) -> None:
            self.content = content
            super().__init__(sender)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.input_field = Input(placeholder="Enter command...", id="input_field")
        self.submit_button = Button(label="Send", id="send_button")

    def compose(self):
        yield Horizontal(self.input_field, self.submit_button)

    def on_mount(self) -> None:
        self.styles.height = 3
        self.styles.width = "100%"
        self.styles.border = ("round", "#5f5fa0")
        self.styles.padding = (0, 1)
        self.styles.background = "#202030"
        self.input_field.styles.background = "#1c1c2b"
        self.submit_button.styles.background = "#1c1c2b"
        self.submit_button.styles.color = "#cccccc"
        self.input_field.styles.color = "#cccccc"
        self.input_field.styles.border = None
        self.input_field.styles.padding = (0, 1)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.post_message(self.Submitted(self, self.input_field.value))
        self.input_field.value = ""


# MenuOverlay widget for displaying the sidebar menu options

class MenuOverlay(Static):
    def compose(self):
        yield Vertical(
            Button("📡 Радиоэфир", id="radio"),
            Button("📜 Последние сообщения", id="messages"),
            Button("📁 История запросов", id="history"),
            Button("⚙ Настройки", id="settings"),
            Button("❌ Закрыть меню", id="close"),
            id="menu_column"
        )

def on_mount(self):
    self.styles.width = 40
    self.styles.height = "auto"
    self.styles.border = ("round", "#5f5fa0")
    self.styles.padding = (1, 2)
    self.styles.background = "#202030"

    # 1) абсолютное позиционирование
    self.styles.position = "absolute"
    # 2) ставим центр экрана
    self.styles.left = "50%"
    self.styles.top = "50%"
    # 3) смещаем назад половину своих размеров
    self.styles.translate_x = "-50%"
    self.styles.translate_y = "-50%"

    # 4) поверх всех остальных
    self.styles.z = 10
