import requests
from tqdm import tqdm
import time
import pandas as pd

members = {789656041423896587: 'Cozy Bearrrrr',
           679677307300216841: 'UnbeatableVN',
           764194057378856961: '3 Giờ Rửa Chim',
           599076572745695233: 'Lushen2711',
           815706256463364116: 'Sứ Giả Lọk Khe'}


def get_puuid(summoner_name, region, api_key):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    )
    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid


def get_match_ids(puuid, mass_region, no_games, queue_id, api_key):
    api_url = (
        "https://" +
        mass_region +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid +
        "/ids?start=0" +
        "&count=" +
        str(no_games) +
        "&queue=" +
        str(queue_id) +
        "&api_key=" +
        api_key
    )

    # print(f"REQUEST URL: {api_url}")

    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids


def get_match_data(match_id, mass_region, api_key):
    api_url = (
        "https://" +
        mass_region +
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id +
        "?api_key=" +
        api_key
    )

    # we need to add this "while" statement so that we continuously loop until it's successful
    while True:
        resp = requests.get(api_url)

        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 10 seconds")
            time.sleep(10)
            # continue means start the loop again
            continue

        match_data = resp.json()
        return match_data


def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data


def get_team_kills(match_data, teamid):
    res = 0
    for p in match_data['info']['participants']:
        if p['teamId'] == teamid:
            res += p['kills']
    return res


def gather_all_data(puuid, match_ids, mass_region, api_key):
    # We initialise an empty dictionary to store data for each game
    data = {
        'champion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': [],
        'dmg': [],
        'pentakill': [],
        'teamkills': []
    }

    for match_id in tqdm(match_ids):
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)

        # assign the variables we're interested in
        champion = player_data['championName']
        k = player_data['kills']
        d = player_data['deaths']
        a = player_data['assists']
        win = player_data['win']
        dmg = player_data['totalDamageDealtToChampions']
        penta = player_data['pentaKills']
        teamid = player_data['teamId']

        # add them to our dataset
        data['champion'].append(champion)
        data['kills'].append(k)
        data['deaths'].append(d)
        data['assists'].append(a)
        data['win'].append(win)
        data['dmg'].append(dmg)
        data['pentakill'].append(penta)
        data['teamkills'].append(get_team_kills(match_data, teamid))

    df = pd.DataFrame(data)
    df['participation'] = (df['kills'] + df['assists']) / df['teamkills'] * 100

    return df
