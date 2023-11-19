import base64
import psutil
import requests
import json
from urllib.parse import urlencode
from utils import scan_client_instances

class LCU:
    def __init__(self, name):
        self.name = name
        self.client_instances = scan_client_instances(name)

    @staticmethod
    def get_players_data(token, port):
        headers_riot = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'LeagueOfLegendsClient',
            'Authorization': 'Basic ' + token,
        }

        api_champ_select = f"https://127.0.0.1:{port}/chat/v5/participants/champ-select"
        # Get request to api
        r = requests.get(api_champ_select, verify=False, headers=headers_riot)
        data = json.loads(r.text)
        # Parsing the names
        participant_names = {pax['name'] for pax in data['participants']}
        player_names = list(participant_names)

        return player_names

    def get_opgg_link(self):

        base_url = f'https://www.op.gg/multisearch/{self.region}?'
        params = {'summoners': ','.join(self.player_names)}

        return base_url + urlencode(params)

    def get_ugg_link(self):

        formatted_regions = {
            'eune': 'eun1',
            'euw': 'euw1',
            'na': 'na1',
            'br': 'br1',
            'jp': 'jp1',
            'kr': 'kr'
        }

        base_url = 'https://u.gg/multisearch?'
        params = {
            'summoners': ','.join(self.player_names),
            'region': formatted_regions.get(self.region, '')
        }

        return base_url + urlencode(params, safe=',')

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

