from flet import UserControl, Column, Container, Row, RadialGradient, Alignment, ElevatedButton, colors, TextButton, AlertDialog, Text
from lcu import LCU
import webbrowser


class App(UserControl):
    def build(self):
        # Button list of players
        self.p1 = TextButton(text='N/A', data='p1')
        self.p2 = TextButton(text='N/A', data='p2')
        self.p3 = TextButton(text='N/A', data='p3')
        self.p4 = TextButton(text='N/A', data='p4')
        self.p5 = TextButton(text='N/A', data='p5')
        # TODO: Player buttons should open OP.GG Profile

        # Instantiating the LCU class
        self.instance = LCU('LeagueClientUx.exe')
        # Getting client info
        self.instance.get_client_data()

        # Main Nav View
        return Column(
            controls=[
                # Main Container
                Container(
                    width=400,
                    height=800,
                    gradient=RadialGradient(
                        center=Alignment(0, -1.25),
                        radius=1.4,
                        colors=[
                            '#42445f',
                            '#393b52',
                            '#33354a',
                            '#2f3143',
                            '#292b3c',
                            '#222331',
                            '#1a1a25',
                            '#1a1b26',
                            '#21222f',
                            '#1d1e2a',
                        ]
                    ),
                    margin=-10,
                    padding=25,
                    # Main Column
                    content=Column(
                        controls=[
                            # Buttons Container
                            Container(
                                width=400,
                                height=200,

                                content=Row(
                                    alignment='center',
                                    spacing=20,

                                    controls=[
                                        # OP.GG Button
                                        ElevatedButton(
                                            text='OP.GG',
                                            bgcolor=colors.BLUE_GREY_100,
                                            color=colors.BLACK,
                                            on_click=self.button_clicked,
                                            data='OP.GG',

                                        ),
                                        # Get Names Button
                                        ElevatedButton(

                                            text='Get Names',
                                            bgcolor=colors.BLUE_GREY_100,
                                            color=colors.BLACK,
                                            on_click=self.button_clicked,
                                            data='Get Names',
                                        ),
                                        ElevatedButton(
                                            text='U.GG',
                                            bgcolor=colors.BLUE_GREY_100,
                                            color=colors.BLACK,
                                            on_click=self.button_clicked,
                                            data='U.GG'
                                        )
                                    ]
                                )
                            ),
                            # Player List Container
                            Container(
                                width=400,
                                height=500,
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=50,

                                    controls=[
                                        # Player 1 Button
                                        self.p1,
                                        # Player 2 Button
                                        self.p2,
                                        # Player 3 Button
                                        self.p3,
                                        # Player 4 Button
                                        self.p4,
                                        # Player 5 Button
                                        self.p5
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def button_clicked(self, e):


        data = e.control.data
        if data == 'Get Names':
            # Reset the array
            self.instance.reset_player_list()

            # Get names of people
            players_names = self.instance.get_players_data()

            self.p1.text = players_names[0]
            self.p2.text = players_names[1]
            self.p3.text = players_names[2]
            self.p4.text = players_names[3]
            self.p5.text = players_names[4]
        elif data == 'OP.GG':
            url = self.instance.get_opgg_link()
            webbrowser.open(url=url, new=0, autoraise=True)
        elif data == 'U.GG':
            url = self.instance.get_ugg_link()
            webbrowser.open(url=url, new=0, autoraise=True)

        elif data == 'p1':
            print(self.p1.text)

        self.update()

