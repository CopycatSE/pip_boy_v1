import webview
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    webview.create_window("My Desktop App", app, width=800, height=600)
    webview.start()
