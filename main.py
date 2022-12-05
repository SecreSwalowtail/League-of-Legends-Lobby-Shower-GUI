import time
import flet
from flet import Page
from app import App
import lcu


def main(page: Page):
    page.title = 'League of Legends - Lobby Shower'
    page.window_height = 800
    page.window_width = 400

    # Check if client is open and throw error
    err1 = flet.AlertDialog(
        title=flet.Text('League Client not found. Make sure to run the client first.', text_align='center'))

    if lcu.LCU.check_client_running('LeagueClientUx.exe') == False:
        page.dialog = err1
        err1.open = True
        page.update()
        time.sleep(2)
        page.window_close()
    else:
        pass

    # TODO: Notifications when not in champion select

    # Main Window Elements
    app = App()
    page.add(app)


flet.app(target=main)
