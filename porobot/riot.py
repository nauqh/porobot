import requests
from tqdm import tqdm
import time
import pandas as pd


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

    print(f"REQUEST URL: {api_url}")

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


def gather_data(puuid, match_ids, mass_region, api_key):
    matches = []
    player = []
    for match_id in tqdm(match_ids):
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)
        matches.append(match_data['info'])
        player.append(player_data)

    # Dataframe of all players of 5 games (5 x 10 records)
    df = pd.json_normalize(matches, record_path=['participants'])
    # Dataframe of player of 5 games
    player_df = pd.json_normalize(player)
    return df, player_df


def progress_bar(percent: float) -> str:
    progress = ''
    for i in range(12):
        if i == (int)(percent*12):
            progress += '🔘'
        else:
            progress += '▬'
    return progress


def transform(df: pd.DataFrame):
    stats = {}
    # KDA
    stats['kills'] = df['kills'].mean()
    stats['deaths'] = df['deaths'].mean()
    stats['assists'] = df['assists'].mean()

    # Champions
    stats['champions'] = df['championName'].tolist()

    # Damage, Penta, Games
    stats['dmg'] = df['totalDamageDealtToChampions'].mean()  # Dmg
    stats['penta'] = df['pentaKills'].sum()  # Penta
    stats['wins'] = df['win'].value_counts().values[0]  # Wins
    stats['loses'] = df['win'].value_counts().values[1]  # Loses

    # Achievements (time in sec)
    stats['timealive'] = df['longestTimeSpentLiving'].mean()
    stats['timedead'] = df['totalTimeSpentDead'].mean()
    stats['totalheal'] = df['totalHealsOnTeammates'].mean()
    stats['cs'] = df['totalMinionsKilled'].mean()
    return stats


if __name__ == "__main__":
    api_key = "RGAPI-a384a673-d288-42ec-a860-55a1602dba94"
    summoner_name = 'Sứ Giả Lọk Khe'
    region = 'vn2'
    mass_region = "sea"
    no_games = 5
    queue_id = 450

    puuid = get_puuid(summoner_name, region, api_key)
    match_ids = get_match_ids(puuid, mass_region, no_games, queue_id, api_key)
    games, df = gather_data(puuid, match_ids, mass_region, api_key)
