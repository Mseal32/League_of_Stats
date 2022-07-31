import dearpygui.dearpygui as dpg
import modules.json_manager as json_manager

player_list = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8", "Player9", "Player10"]
blue_team = player_list[0:5]
red_team = player_list[5:10]

dpg.create_context()


def manual_entry_match_summary():
    help_color = [55, 60, 255]
    with dpg.window(label="Modify Stats", tag="Modify Stats", pos=[700, 100], on_close=cleanup_tags_modify_stats):
        with dpg.group(horizontal=True):
            dpg.add_text("      NAME", color=help_color)
            dpg.add_text("            K", color=help_color)
            dpg.add_text("  D", color=help_color)
            dpg.add_text("  A", color=help_color)
            dpg.add_text("  CS", color=help_color)
            dpg.add_text("  GOLD", color=help_color)
            dpg.add_text("    CHAMPION", color=help_color)
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value="Team 1", tag="Team 1", width=300)
        for blue_player in blue_team:
            dpg.add_group(horizontal=True, tag=blue_player)
            dpg.add_input_text(default_value="", width=150, parent=blue_player)
            dpg.add_input_text(default_value="", width=20, parent=blue_player)
            dpg.add_input_text(default_value="", width=20, parent=blue_player)
            dpg.add_input_text(default_value="", width=20, parent=blue_player)
            dpg.add_input_text(default_value="", width=30, parent=blue_player)
            dpg.add_input_text(default_value="", width=50, parent=blue_player)
            dpg.add_input_text(parent=blue_player)

        with dpg.group(horizontal=True):
            dpg.add_text("------------------------------------------------------------")
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value="Team 2", tag="Team 2", width=300)
        for red_player in red_team:
            dpg.add_group(horizontal=True, tag=red_player)
            dpg.add_input_text(default_value="", width=150, parent=red_player)
            dpg.add_input_text(default_value="", width=20, parent=red_player)
            dpg.add_input_text(default_value="", width=20, parent=red_player)
            dpg.add_input_text(default_value="", width=20, parent=red_player)
            dpg.add_input_text(default_value="", width=30, parent=red_player)
            dpg.add_input_text(default_value="", width=50, parent=red_player)
            dpg.add_input_text(parent=red_player)
        dpg.add_button(indent=250, label="Apply & Close", callback=lambda: manual_entry_confirm_choices())


def manual_entry_existing_teams():
    help_color = [55, 60, 255]
    team_data = json_manager.get_team_data()
    teams = list(team_data)
    with dpg.window(label="Modify Stats", tag="Modify Stats", pos=[700, 100], on_close=cleanup_tags_modify_stats):
        with dpg.group(horizontal=True):
            dpg.add_text("      NAME", color=help_color)
            dpg.add_text("            K", color=help_color)
            dpg.add_text("  D", color=help_color)
            dpg.add_text("  A", color=help_color)
            dpg.add_text("  CS", color=help_color)
            dpg.add_text("  GOLD", color=help_color)
            dpg.add_text("    CHAMPION", color=help_color)
        with dpg.group(horizontal=True):
            dpg.add_combo(label="Team 1", tag="Team 1", items=teams, callback=update_players_existing_teams)


def update_players_existing_teams(sender, app_data, user_data):
    team_name = app_data
    team_data = json_manager.get_team_data()
    teams = list(team_data)
    players = json_manager.get_team_data()[team_name]["Players"]
    sender_name = dpg.get_item_label(sender)

    if sender_name == "Team 1":
        parent = dpg.get_item_parent(dpg.get_item_parent(sender))
    elif sender_name == "Team 2":
        parent = dpg.get_item_parent(sender)
    dpg.delete_item(sender)

    if sender_name == "Team 1":
        with dpg.group(horizontal=True, parent=parent):
            dpg.add_text("Team 1: " + team_name, color=[0, 0, 255], tag="Team1Name")
    elif sender_name == "Team 2":
        with dpg.group(horizontal=True, parent=parent):
            dpg.add_text("Team 2: " + team_name, color=[255, 0, 0], tag="Team2Name")

    for player in players:
        dpg.add_group(horizontal=True, parent=parent, tag=player)
        dpg.add_input_text(default_value=player, width=150, parent=player)
        dpg.add_input_text(default_value="", width=20, parent=player)
        dpg.add_input_text(default_value="", width=20, parent=player)
        dpg.add_input_text(default_value="", width=20, parent=player)
        dpg.add_input_text(default_value="", width=30, parent=player)
        dpg.add_input_text(default_value="", width=50, parent=player)
        dpg.add_input_text(parent=player)

    if sender_name == "Team 1":
        dpg.add_separator(parent=parent)
        dpg.add_combo(label="Team 2", tag="Team 2", parent=parent, items=teams, callback=update_players_existing_teams)
    elif sender_name == "Team 2":
        team1_name = dpg.get_value("Team1Name").split(": ")[1]
        team2_name = dpg.get_value("Team2Name").split(": ")[1]
        dpg.add_button(indent=260, label="Apply and Close", parent=parent,
                       callback=lambda: manual_entry_confirm_choices(teams=[team1_name, team2_name], dpg_window=parent))


def process_player_info(pre_player_info, player_list):
    global blue_team
    for player in player_list:
        for kda in range(len(pre_player_info[player][1]) + 1):
            if kda == 2:
                pre_player_info[player][1].append("0")
    return pre_player_info


def cleanup_tags_modify_stats():
    dpg.delete_item("Modify Stats")
    for player in player_list:
        if dpg.does_alias_exist(player):
            dpg.remove_alias(player)
    if dpg.does_alias_exist("Team 1"):
        dpg.remove_alias("Team 1")
    if dpg.does_alias_exist("Team 2"):
        dpg.remove_alias("Team 2")


def manual_entry_confirm_choices(teams: list = None, dpg_window=None):
    if teams is None:
        teams = [dpg.get_value("Team 1"), dpg.get_value("Team 2")]

    player_stats = []
    test_list = []
    pointer = 1

    if dpg_window is None:
        for player in player_list:
            for item in dpg.get_item_children(player)[1]:
                player_stats.append(dpg.get_value(item))
            if player in blue_team:
                player_stats.append(True)
                player_stats.append(teams[0])
            else:
                player_stats.append(False)
                player_stats.append(teams[1])

        for stat in player_stats:
            if pointer % 9 == 0:
                test_list.append(stat)
                json_manager.add_player_to_json(test_list)
                test_list.clear()
            else:
                test_list.append(stat)
            pointer += 1

        json_manager.update_team_data(player_stats, teams)


    else:
        for item in dpg.get_item_children(dpg_window)[1]:
            if dpg.get_item_type(item) == "mvAppItemType::mvGroup":
                for value in dpg.get_item_children(item)[1]:
                    player_stats.append(dpg.get_value(value))

        for remove_item in range(7):
            player_stats.pop(0)

        team_1 = []
        for stat in range(36):
            team_1.append(player_stats[stat])
        team_2 = []
        for stat in range(36, len(player_stats)):
            team_2.append(player_stats[stat])
        print(team_1)
        print(team_2)
        json_manager.add_player_to_json_existing_teams(team_1, team_2)

    # global player_list
    # player_list = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8", "Player9", "Player10"]


    cleanup_tags_modify_stats()


def add_solo_player():
    with dpg.window(label="Adding/Updating (No Team) Player"):
        with dpg.group(horizontal=True):
            dpg.add_text("Existing Player")
            name_checkbox = dpg.add_checkbox(callback=toggle_existing_solo_player)
            dpg.add_text("                  ")
        with dpg.group(horizontal=True):
            dpg.add_text("      NAME")
            dpg.add_text("         K")
            dpg.add_text("  D")
            dpg.add_text("  A")
            dpg.add_text("   CS")
            dpg.add_text("    GOLD")
            dpg.add_text("    CHAMPION")
        with dpg.group(horizontal=True):
            name_input_text = dpg.add_input_text(default_value="", width=120)
            name_combo = dpg.add_combo(items=[], show=False, width=120)
            kills = dpg.add_input_text(width=25)
            deaths = dpg.add_input_text(width=25)
            assists = dpg.add_input_text(width=25)
            cs = dpg.add_input_text(width=35)
            gold = dpg.add_input_text(width=70)
            champion = dpg.add_input_text()
        dpg.add_separator()
        with dpg.group(horizontal=True):
            won_game = dpg.add_checkbox(label="Won Game")
            dpg.add_text("                   ")
            dpg.add_button(label="Apply and Close",
                           callback=lambda: add_solo_player_confirm_choices(name_checkbox, [name_input_text, name_combo], kills, deaths, assists, cs, gold, champion,
                                                                            won_game))

    dpg.set_item_user_data(name_checkbox, [name_input_text, name_combo])


def toggle_existing_solo_player(sender, appdata, user_data):
    if dpg.does_item_exist(user_data[0]):
        dpg.delete_item(user_data[0])
        dpg.show_item(user_data[1])
        dpg.configure_item(sender, enabled=False)


def add_solo_player_confirm_choices(toggle, name, kills, deaths, assists, cs, gold, champion, won_game):
    if dpg.get_value(toggle):
        name = name[1]
    else:
        name = name[0]
    name = dpg.get_value(name)
    won_game = dpg.get_value(won_game)
    if won_game:
        won_game = 1
    else:
        won_game = 0

    kills = dpg.get_value(kills)
    deaths = dpg.get_value(deaths)
    assists = dpg.get_value(assists)
    cs = dpg.get_value(cs)
    gold = dpg.get_value(gold).replace(",", "")
    champion = dpg.get_value(champion)

    json_manager.add_solo_player(name, kills, deaths, assists, cs, gold, champion, won_game)
    dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(toggle)))
