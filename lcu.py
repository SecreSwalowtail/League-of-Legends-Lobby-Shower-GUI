import base64
import psutil
import requests
import json

class LCU:
    lockfile_location = None
    port_number = None
    auth_token = None
    lol_name = None
    cmd = None
    region = None
    remoting_auth_token = None
    riot_client_auth_token = None
    app_port = None
    riot_client_port = None

    lcu_link = None
    riot_link = None

    player_names = []

    def __init__(self, name):
        self.name = name
        for process in psutil.process_iter():
            if process.name() == self.name:
                #  Lockfile is needed to get the port,token and other things from client
                #  This scans the process list , finds the Client name and sets the path to lockfile_location
                for pid in psutil.pids():
                    if psutil.Process(pid).name() == name:
                        temp = psutil.Process(pid).exe()
                        temp2 = temp.replace('\\', '/')
                        temp3 = temp2.replace('LeagueClientUx.exe', '')
                        self.lockfile_location = temp3 + 'lockfile'

                # This will get all info from cmd , like riot port, riot token etc...
                for i in psutil.process_iter():
                    if i.name() == name:
                        self.cmd = i.cmdline()

                for line in self.cmd:
                    if '--region=' in line:
                        self.region = line.split('--region=', 1)[1].lower()
                    if '--remoting-auth-token=' in line:
                        self.auth_token = line.split('--remoting-auth-token=', 1)[1]
                    if '--app-port=' in line:
                        self.app_port = line.split('--app-port=', 1)[1]
                    if '--riotclient-auth-token=' in line:
                        self.riot_client_auth_token = line.split('--riotclient-auth-token=', 1)[1]
                    if '--riotclient-app-port=' in line:
                        self.riot_client_port = line.split('--riotclient-app-port=', 1)[1]

    def get_client_data(self):
        # Reading the lockfile and appending it
        f = open(self.lockfile_location, 'r')
        data = f.read()
        data = data.split(':')
        self.port_number = data[2]
        # There are 2 tokens available
        # Auth token is for LCU , Riot Client Token is for client
        self.auth_token = base64.b64encode(('riot:' + data[3]).encode('ascii')).decode('ascii')
        self.riot_client_auth_token = base64.b64encode(('riot:' + self.riot_client_auth_token).encode('ascii')).decode(
            'ascii')
        # Setting up some variable that will be used later
        self.lcu_link = 'https://127.0.0.1:' + self.port_number
        self.riot_link = 'https://127.0.0.1:' + self.riot_client_port

    def get_players_data(self):
        # LCU requires this specific header to be sent
        headers_riot = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'LeagueOfLegendsClient',
            'Authorization': 'Basic ' + self.riot_client_auth_token,
        }
        # Full link to get player names
        api_champ_select = self.riot_link + '/chat/v5/participants/champ-select'
        # Get request to api
        r = requests.get(api_champ_select, verify=False, headers=headers_riot)
        data = json.loads(r.text)
        # Parsing the names
        for names in data['participants']:
            # Check if the same name is appending twice
            if names['name'] not in self.player_names:
                self.player_names.append(names['name'])
                #print(names)

        return self.player_names

    def get_opgg_link(self):

        # OPGG link with region included
        temp_link = 'https://www.op.gg/multisearch/' + self.region + '?summoners='
        # Spaces to %20
        first_pass_formated_names = [w.replace(' ', '%20') for w in self.player_names]
        # Joining strings with separator %2C
        second_pass_formated_names = '%2C'.join(first_pass_formated_names)

        opgg = temp_link + second_pass_formated_names
        return opgg

    def get_ugg_link(self):
        formatted_region = ''
        # Translate region to u.gg regions
        if self.region == 'eune':
            formatted_region = 'eun1'
        elif self.region == 'euw':
            formatted_region = 'euw1'
        elif self.region == 'na':
            formatted_region = 'na1'
        elif self.region == 'br':
            formatted_region = 'br1'
        elif self.region == 'jp':
            formatted_region = 'jp1'
        elif self.region == 'kr':
            formatted_region = 'kr'

        temp_link = 'https://u.gg/multisearch?summoners='
        # Spaces to %20
        first_pass_formatted_names = [w.replace(' ', '%20') for w in self.player_names]
        # Joining strings with separator ','
        second_pass_formatted_names = ','.join(first_pass_formatted_names)

        # Combining everything in one link
        temp_link2 = temp_link + second_pass_formatted_names + '&region=' + formatted_region

        return temp_link2

    @staticmethod
    def check_client_running(processname):
        # Error checking if client is open
        for proc in psutil.process_iter():
            try:
                if processname.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def reset_player_list(self):
        # Reset the player list every time button is clicked
        self.player_names.clear()

    def get_opgg_profile(self, n):
        # For each player , open the OP.GG profile in a new tab
        opgg_link = 'https://www.op.gg/summoners/' + self.region + '/' + self.player_names[n]
        return opgg_link

    # TODO: Error checking for 401,403,404

