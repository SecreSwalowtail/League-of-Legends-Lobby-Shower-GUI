import json
import psutil
import base64
import requests

argument_mapping = {
    '--region=': 'region',
    '--remoting-auth-token=': 'auth_token',
    '--app-port=': 'app_port',
    '--riotclient-auth-token=': 'riot_client_auth_token',
    '--riotclient-app-port=': 'riot_client_port',
}


def encode_auth_tokens(token):
    return base64.b64encode(('riot:' + token).encode('ascii')).decode('ascii')


def extract_process_data(process, arguments):
    data = {}
    for line in process.cmdline():
        for argument, attribute in arguments.items():
            if argument in line:
                value = line.split(argument, 1)[1].lower() if attribute == 'region' else line.split(argument, 1)[1]
                if attribute in ['auth_token', 'riot_client_auth_token']:
                    value = encode_auth_tokens(value)
                data[attribute] = value
    return data


def get_instance_player_name(port, token):
    headers_riot = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'LeagueOfLegendsClient',
        'Authorization': 'Basic ' + token,
    }

    url = f"https://127.0.0.1:{port}/lol-summoner/v1/current-summoner"
    r = requests.get(url, verify=False, headers=headers_riot)
    data = json.loads(r.text)
    return data.get('gameName', None)


def scan_client_instances(name):
    client_data = {}

    for process in psutil.process_iter(['cmdline']):
        if process.name() == name:
            data = extract_process_data(process, argument_mapping)
            port = data.get('app_port', None)
            auth_token = data.get('auth_token', None)

            if port and auth_token:
                player_name = get_instance_player_name(port, auth_token)
                if player_name:
                    client_data[player_name] = data

    return client_data
