import json
import pstats

import modules.data_location_preferences as dl
from os.path import abspath

data_folder_path = dl.path_to_data_folder()
player_stats_file_path = data_folder_path + "/player_stats.json"


def get_file_data(file_path):
    try:
        with open(file_path, "r") as file:
            file_data = json.loads(file.read())
    except json.JSONDecodeError:
        with open(file_path, "w") as file:
            file.write("{}")
    return file_data


def get_team_data():
    try:
        with open(dl.path_to_data_folder() + "/teams.json", "r") as file:
            file_data = json.loads(file.read())
    except json.JSONDecodeError:
        print("ERROR getting data from\n\t" + abspath(dl.path_to_data_folder() + "/teams.json") + "\n\n")
        with open(dl.path_to_data_folder() + "/teams.json", "w") as file:
            file.write("{}")
    return file_data


def add_player_to_json(stat_list):
    with open(data_folder_path + "/player_stats.json", "r") as player_data_file:
        player_data_file_data = json.loads(player_data_file.read())
        players = list(player_data_file_data)

    name = stat_list[0]

    gold = stat_list[5].replace(",", "")

    for stat in stat_list[1:6]:
        if stat == "":
            raise ValueError("Missing Value found for " + name)

    kills = int(stat_list[1])
    deaths = int(stat_list[2])
    assists = int(stat_list[3])
    cs = int(stat_list[4])
    gold = int(gold)

    champion = stat_list[6]
    won_game = stat_list[7]
    team = stat_list[8]

    if won_game:
        won_game_placeholder = 1
        loss_game_placeholder = 0
    else:
        won_game_placeholder = 0
        loss_game_placeholder = 1

    if name not in players:
        player_data = {
            name: {
                "Games Won": won_game_placeholder,
                "Games Lost": loss_game_placeholder,
                "Games Played": 1,
                "Winrate": win(won_game),
                "Kills": kills,
                "Deaths": deaths,
                "Assists": assists,
                "KDA Ratio": (kills + assists) / deaths,
                "Average CS": cs,
                "Overall CS": cs,
                "Average Gold Collected": gold,
                "Overall Gold Collected": gold,
                "Team": team
            }
        }
    else:
        current_player_data = player_data_file_data[name]
        player_data = {
            name: {
                "Games Won": current_player_data["Games Won"] + won_game_placeholder,
                "Games Lost": current_player_data["Games Lost"] + loss_game_placeholder,
                "Games Played": current_player_data["Games Played"] + 1,
                "Winrate": ((current_player_data["Games Won"] + won_game_placeholder) / (current_player_data["Games Played"] + 1)),
                "Kills": current_player_data["Kills"] + kills,
                "Deaths": current_player_data["Deaths"] + deaths,
                "Assists": current_player_data["Assists"] + assists,
                "KDA Ratio": ((current_player_data["Kills"] + kills) + (current_player_data["Assists"] + assists)) / (current_player_data["Deaths"] + deaths),
                "Average CS": (current_player_data["Overall CS"] + cs) / (current_player_data["Games Played"] + 1),
                "Overall CS": current_player_data["Overall CS"] + cs,
                "Average Gold Collected": (current_player_data["Overall Gold Collected"] + gold) / (current_player_data["Games Played"] + 1),
                "Overall Gold Collected": current_player_data["Overall Gold Collected"] + gold,
                "Team": team
            }
        }

    with open(player_stats_file_path, "w") as file:
        player_data_file_data.update(player_data)
        json.dump(player_data_file_data, file, indent=2)

    update_champion_data(name, champion, won_game_placeholder, loss_game_placeholder, kills, deaths, assists, cs, gold)


def win(won_game):
    if won_game:
        return 100
    else:
        return 0


def update_champion_data(player_name, champion, won, lost, kills, deaths, assists, cs, gold):
    with open(data_folder_path + "/player_champion_data.json", "r") as champion_file:
        champion_data = json.loads(champion_file.read())
    player_list = list(champion_data)

    if player_name in player_list:
        player_champion_data = champion_data[player_name]
        champions_played = list(player_champion_data)
        if champion in champions_played:
            new_games_played = player_champion_data[champion]["Games Played"] + 1
            new_games_won = player_champion_data[champion]["Games Won"] + won
            new_total_kills = player_champion_data[champion]["Total Kills"] + kills
            new_total_deaths = player_champion_data[champion]["Total Deaths"] + deaths
            new_total_assists = player_champion_data[champion]["Total Assists"] + assists
            new_cs = player_champion_data[champion]["Total CS"] + cs
            new_gold = player_champion_data[champion]["Total Gold"] + gold
            data = {
                champion: {
                    "Winrate": round((new_games_won / new_games_played) * 100, 2),
                    "Games Played": new_games_played,
                    "Games Won": new_games_won,
                    "Games Lost": player_champion_data[champion]["Games Lost"] + lost,
                    "Total Kills": new_total_kills,
                    "Total Deaths": new_total_deaths,
                    "Total Assists": new_total_assists,
                    "Total CS": new_cs,
                    "Total Gold": new_gold,
                    "KDA Ratio": (new_total_kills + new_total_assists) / new_total_deaths,
                    "Average CS": new_cs / new_games_played,
                    "Average Gold": new_gold / new_games_played
                }
            }
        else:
            data = {
                champion: {
                    "Games Played": 1,
                    "Games Won": won,
                    "Games Lost": lost,
                    "Total Kills": kills,
                    "Total Deaths": deaths,
                    "Total Assists": assists,
                    "Total CS": cs,
                    "Total Gold": gold,
                    "KDA Ratio": (kills + assists) / deaths,
                    "Average CS": cs,
                    "Average Gold": gold
                }
            }
        player_champion_data.update(data)
    else:
        data = {
            player_name: {
                champion: {
                    "Games Played": 1,
                    "Games Won": won,
                    "Games Lost": lost,
                    "Total Kills": kills,
                    "Total Deaths": deaths,
                    "Total Assists": assists,
                    "Total CS": cs,
                    "Total Gold": gold,
                    "KDA Ratio": (kills + assists) / deaths,
                    "Average CS": cs,
                    "Average Gold": gold
                }
            }
        }
        champion_data.update(data)

    with open(data_folder_path + "/player_champion_data.json", "w") as file:
        json.dump(champion_data, file, indent=2)


def add_player_to_json_existing_teams(team_1, team_2):
    team_1_name = team_1.pop(0).split(":")[1].strip()
    team_2_name = team_2.pop(0).split(":")[1].strip()

    team_1_list = []
    player_1 = team_1[0:7]
    player_2 = team_1[7:14]
    player_3 = team_1[14:21]
    player_4 = team_1[21:28]
    player_5 = team_1[28: 35]
    team_1_list.append(player_1)
    team_1_list.append(player_2)
    team_1_list.append(player_3)
    team_1_list.append(player_4)
    team_1_list.append(player_5)

    team_2_list = []
    player_6 = team_2[0:7]
    player_7 = team_2[7:14]
    player_8 = team_2[14:21]
    player_9 = team_2[21:28]
    player_10 = team_2[28: 35]
    team_2_list.append(player_6)
    team_2_list.append(player_7)
    team_2_list.append(player_8)
    team_2_list.append(player_9)
    team_2_list.append(player_10)

    for player in team_1_list:
        player.append(True)
        player.append(team_1_name)
        add_player_to_json(player)

    for player in team_2_list:
        player.append(False)
        player.append(team_2_name)
        add_player_to_json(player)

    player_stats = []
    player_stats.extend(player_1)
    player_stats.extend(player_2)
    player_stats.extend(player_3)
    player_stats.extend(player_4)
    player_stats.extend(player_5)
    player_stats.extend(player_6)
    player_stats.extend(player_7)
    player_stats.extend(player_8)
    player_stats.extend(player_9)
    player_stats.extend(player_10)

    update_team_data(player_stats, [team_1_name, team_2_name])


def update_team_data(player_stats, teams):
    team_data = get_file_data(data_folder_path + "/teams.json")
    p_one = player_stats[0:9]
    p_two = player_stats[9:18]
    p_three = player_stats[18: 27]
    p_four = player_stats[27: 36]
    p_five = player_stats[36: 45]
    p_six = player_stats[45: 54]
    p_seven = player_stats[54: 63]
    p_eight = player_stats[63: 72]
    p_nine = player_stats[72: 81]
    p_ten = player_stats[81:90]
    players = [p_one, p_two, p_three, p_four, p_five, p_six, p_seven, p_eight, p_nine, p_ten]
    for player in range(len(players)):
        players[player] = players[player][0]
    team_1_players = players[0:5]
    team_2_players = players[5:10]

    team_1 = teams[0]
    team_2 = teams[1]
    if team_1 not in list(team_data):
        team_1_data = {
            team_1: {
                "Players": team_1_players,
                "Games Won": 1,
                "Games Lost": 0,
                "Games Played": 1
            }
        }
    else:
        team_1_data = {
            team_1: {
                "Players": team_1_players,
                "Games Won": team_data[team_1]["Games Won"] + 1,
                "Games Lost": team_data[team_1]["Games Lost"],
                "Games Played": team_data[team_1]["Games Played"] + 1
            }
        }
    if team_2 not in list(team_data):
        team_2_data = {
            team_2: {
                "Players": team_2_players,
                "Games Won": 0,
                "Games Lost": 1,
                "Games Played": 1
            }
        }
    else:
        team_2_data = {
            team_2: {
                "Players": team_2_players,
                "Games Won": team_data[team_2]["Games Won"],
                "Games Lost": team_data[team_2]["Games Lost"] + 1,
                "Games Played": team_data[team_2]["Games Played"] + 1
            }
        }
    team_data.update(team_1_data)
    team_data.update(team_2_data)
    with open(data_folder_path + "/teams.json", "w") as team_file:
        json.dump(team_data, team_file, indent=2)


def add_solo_player(name, kills, deaths, assists, cs, gold, champion, won_game):
    player_data = get_file_data(data_folder_path + "/player_stats.json")
    kills = int(kills)
    deaths = int(deaths)
    assists = int(assists)
    cs = int(cs)
    gold = int(gold)
    if won_game != "1":
        lost_game = 1
    else:
        lost_game = 0

    if name not in list(player_data):
        data = {
            name: {
                "Games Won": won_game,
                "Games Lost": lost_game,
                "Games Played": 1,
                "Winrate": won_game * 100,
                "Kills": kills,
                "Deaths": deaths,
                "Assists": assists,
                "KDA Ratio": (kills + assists) / deaths,
                "Average CS": cs,
                "Overall CS": cs,
                "Average Gold Collected": gold,
                "Overall Gold Collected": gold,
                "Team": "Solo"
            }
        }
    if name in list(player_data) and player_data[name]["Team"] == "Solo":
        player_stats = player_data[name]
        data = {
            name: {
                "Games Won": player_stats["Games Won"] + won_game,
                "Games Lost": player_stats["Games Lost"] + lost_game,
                "Games Played": player_stats["Games Played"] + 1,
                "Winrate": round((player_stats["Games Won"] / player_stats["Games Played"]) * 100, 2),
                "Kills": player_stats["Kills"] + kills,
                "Deaths": player_stats["Deaths"] + deaths,
                "Assists": player_stats["Assists"] + assists,
                "KDA Ratio": ((player_stats["Kills"] + kills) + (player_stats["Assists"] + assists)) / (player_stats["Deaths"] + deaths),
                "Average CS": (player_stats["Average CS"] + cs) / (player_stats["Games Played"] + 1),
                "Overall CS": player_stats["Overall CS"] + cs,
                "Average Gold Collected": (player_stats["Average Gold Collected"] + gold) / (player_stats["Games Played"] + 1),
                "Overall Gold Collected": player_stats["Overall Gold Collected"] + gold,
                "Team": "Solo"
            }
        }

    if name in list(player_data) and player_data[name]["Team"] != "Solo":
        print("Player: '" + name + "' detected on team")
        return
    with open(data_folder_path + "/player_stats.json", "w") as player_stats_file:
        player_data.update(data)
        json.dump(player_data, player_stats_file, indent=2)
    update_champion_data(name, champion, won_game, lost_game, kills, deaths, assists, cs, gold)


def player_champion_stats_to_tuple(player_name: str, player_accepted_stats: list, champion_accepted_stats: list):
    try:
        file_data = json.loads(open(data_folder_path + "/player_stats.json").read())
    except json.JSONDecodeError:
        raise ValueError("Error reading data from '" + data_folder_path + "/player_stats.json" + "'\n"
                                                                                                 "If file is empty, add {}")
    try:
        champion_data = json.loads(open(data_folder_path + "/player_champion_data.json").read())
    except json.JSONDecodeError:
        raise ValueError("Error reading data from '" + data_folder_path + "/player_champion_data.json" + "'\n"
                                                                                                         "If file is empty, add {}")
    file_data = file_data[player_name]
    champion_data = champion_data[player_name]
    master_dict = {}
    stats = []
    stat_values = []
    for key, value in file_data.items():
        if key not in player_accepted_stats:
            continue
        stats.append(key)
        stat_values.append(value)
        master_dict[player_name] = (tuple(stats), tuple(stat_values))
    stats.clear()
    stat_values.clear()

    for champion in list(champion_data):
        for key, value in champion_data[champion].items():
            if key not in champion_accepted_stats:
                continue
            stats.append(key)
            stat_values.append(value)
        master_dict[champion] = (tuple(stats), tuple(stat_values))
    stats.clear()
    stat_values.clear()
    return master_dict


def team_player_stats_to_tuple(accepted_stats: list, team_name: str = "Solo"):
    try:
        file_data = json.loads(open(data_folder_path + "/player_stats.json").read())
    except json.JSONDecodeError:
        raise ValueError("Error reading data from '" + data_folder_path + "/player_stats.json" + "'\n"
                                                                                                 "If file is empty, add {}")
    master_dict = {}
    stats = []
    stat_values = []
    for player in list(file_data):
        if team_name != file_data[player]["Team"]:
            continue
        stats.append("Player Name")
        stat_values.append(player)
        for key, value in file_data[player].items():
            if key not in accepted_stats:
                continue
            stats.append(key)
            stat_values.append(value)
        master_dict[player] = (tuple(stats), tuple(stat_values))
        stats.clear()
        stat_values.clear()

    return master_dict


def team_stats_to_tuple(accepted_stats, team_name):
    try:
        file_data = json.loads(open(data_folder_path + "/teams.json").read())
    except json.JSONDecodeError:
        raise ValueError("Error reading data from '" + data_folder_path + "/teams.json" + "'\n"
                                                                                          "If file is empty, add {}")
    master_dict = {}
    stats = []
    stat_values = []
    stats.append("Winrate")
    stat_values.append(round((file_data[team_name]["Games Won"] / file_data[team_name]["Games Played"]) * 100, 2))
    for key, value in file_data[team_name].items():
        if key not in accepted_stats:
            continue
        stats.append(key)
        stat_values.append(value)
    master_dict[team_name] = (tuple(stats), tuple(stat_values))

    return master_dict
