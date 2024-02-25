import time
import requests
import pandas as pd
from tqdm import tqdm


class MissingRegionError(Exception):
    pass


class MissingQueueError(Exception):
    pass


def get_puuid(api_key, summoner, tagline) -> str:
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner}/{tagline}?api_key={api_key}"
    resp = requests.get(url).json()
    return resp['puuid']


def get_info(api_key, puuid, region) -> dict:
    url = f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    resp = requests.get(url)
    if resp.status_code == 404:
        raise KeyError("Summoner not found")
    return resp.json()


def get_rank(api_key, info: dict, region) -> list[dict]:
    url = f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{info['id']}?api_key={api_key}"
    resp = requests.get(url)
    if resp.status_code == 404:
        raise KeyError("Summoner not found")
    return resp.json()


def get_match_ids(api_key, puuid, no_games, queue_id) -> list:
    url = f"https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={no_games}&api_key={api_key}&queue={queue_id}"
    resp = requests.get(url)
    return resp.json()


def get_match_data(api_key, match_id) -> dict:
    url = f"https://sea.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"

    while True:
        resp = requests.get(url)

        if resp.status_code == 429:
            print("Rate Limit hit, sleeping for 10 seconds")
            time.sleep(10)
            continue

        match_data = resp.json()
        return match_data


def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data


def gather_data(api_key, puuid, match_ids):
    matches = []
    player = []
    for match_id in tqdm(match_ids):
        match_data = get_match_data(api_key, match_id)
        player_data = find_player_data(match_data, puuid)
        matches.append(match_data['info'])
        player.append(player_data)

    # Dataframe of all players of 5 games (5 x 10 records)
    match_df = pd.json_normalize(matches)
    # Dataframe of player of 5 games
    player_df = pd.json_normalize(player)
    return match_df, player_df


def transform(match_df: pd.DataFrame, player_df: pd.DataFrame):
    stats = {}

    # KDA
    stats.update({
        'kills': player_df['kills'].mean(),
        'deaths': player_df['deaths'].mean(),
        'assists': player_df['assists'].mean(),
    })

    # Champions
    stats['champions'] = set(player_df['championName'].tolist())

    # Damage, Penta, Games
    stats.update({
        'dmg': player_df['totalDamageDealtToChampions'].mean(),
        'penta': player_df['pentaKills'].sum(),
        'wins': player_df['win'].value_counts().to_dict()[True],
        'loses': player_df['win'].value_counts().to_dict()[False],
    })

    # Achievements (time in sec)
    stats.update({
        'timealive': player_df['longestTimeSpentLiving'].mean() // 60,
        'timedead': player_df['totalTimeSpentDead'].mean(),
        'totalheal': player_df['totalHealsOnTeammates'].max(),
        'cs': player_df['totalMinionsKilled'].mean() + player_df['neutralMinionsKilled'].mean(),
    })

    stats['cspermin'] = ((player_df['totalMinionsKilled'] + player_df['neutralMinionsKilled']) /
                         (match_df['gameDuration'] / 60)).mean()
    stats['vision'] = player_df['visionScore'].mean()
    stats['objsStolen'] = player_df['objectivesStolen'].max()

    return stats


def progress_bar(percent: float) -> str:
    progress = ''
    for i in range(12):
        if i == (int)(percent*12):
            progress += '🔘'
        else:
            progress += '▬'
    return progress


if __name__ == '__main__':
    KEY = 'RGAPI-a384a673-d288-42ec-a860-55a1602dba94'
    summoner = 'Obiwan'
    tagline = 'HYM'
    no_games = 10
    region = "VN2"

    puuid = get_puuid(KEY, summoner, tagline)
    summoner = get_info(KEY, puuid, region)
    print(summoner)
    ids = get_match_ids(KEY, puuid, no_games, 440)

    data = get_match_data(KEY, ids[0])
    player_data = find_player_data(data, puuid)
