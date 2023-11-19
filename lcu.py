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

    @staticmethod
    def get_opgg_link(region, player_names):

        base_url = f'https://www.op.gg/multisearch/{region}?'
        params = {'summoners': ','.join(player_names)}

        return base_url + urlencode(params)

    @staticmethod
    def get_ugg_link(region, player_names):

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
            'summoners': ','.join(player_names),
            'region': formatted_regions.get(region, '')
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

    @staticmethod
    def get_opgg_profile(region, player_name):
        # For each player , open the OP.GG profile in a new tab
        opgg_link = 'https://www.op.gg/summoners/' + region + '/' + player_name
        return opgg_link

    # TODO: Error checking for 401,403,404
