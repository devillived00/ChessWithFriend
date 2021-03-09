from chessdotcom import get_leaderboards


def top_10_players():
    leaderboard = get_leaderboards().json
    players = []
    for i, entry in enumerate(leaderboard['live_blitz']):
        if i < 10:
            players.append(f'{entry["rank"]} | {entry["username"]} | {entry["score"]} |')
    return players
