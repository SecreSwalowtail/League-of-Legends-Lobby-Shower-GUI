import time
import flet
from flet import Page, Banner, colors, TextAlign
from app import App
import lcu
from lcu import LCU


def main(page: Page):
    page.title = 'League of Legends - Lobby Shower'
    page.window_height = 800
    page.window_width = 400
    page.window_resizable = False
    page.window_minimizable = True
    page.window_maximizable = False

    client_detected = False # Constant to track the client state

    # Check if client is open and throw error
    err1 = flet.AlertDialog(
        title=flet.Text('League Client not found.\n Retrying...', text_align=TextAlign.CENTER))

    while not client_detected:
        if lcu.LCU.check_client_running('LeagueClientUx.exe'):
            client_detected = True
        else:
            page.dialog = err1
            err1.open = True
            page.update()

        time.sleep(1)

    # Close the banner when the process is found
    err1.open = False
    page.update()

    # Main Window Elements
    app = App()
    page.add(app)


flet.app(target=main)
