import dearpygui.dearpygui as dpg
import modules.json_manager as jman
import modules.data_location_preferences as dl

path_to_data_folder = dl.path_to_data_folder()


def click_event_show_player_stats(sender, appdata):
    processed_item_tag = appdata[1].split(":")
    player_name = processed_item_tag[1]
    player_stats = jman.get_file_data(path_to_data_folder + "/player_stats.json")[player_name]
    with dpg.window(label=player_name + "'s Stats"):
        with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Stat")
            dpg.add_table_column(label="Quantity")
            for stat in player_stats:
                if stat == "Team":
                    continue
                with dpg.table_row():
                    with dpg.table_cell():
                        dpg.add_selectable(label=stat)
                    for col in range(1):
                        with dpg.table_cell():
                            dpg.add_selectable(label=player_stats[stat])
        dpg.add_text("------------------------------------------------")
        dpg.add_button(label="View Champion Stats", callback=lambda: show_player_champion_stats(player_name))


def click_event_show_player_champion_stats(sender, appdata):
    processed_item_tag = appdata[1].split(":")
    player = processed_item_tag[0]
    champion = processed_item_tag[1]
    champion_stats = jman.get_file_data(path_to_data_folder + "/player_champion_data.json")[player][champion]
    with dpg.window(label=player + "'s " + champion + "'s " + "Stats"):
        with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Stat")
            dpg.add_table_column(label="Quantity")
            for stat in champion_stats:
                with dpg.table_row():
                    with dpg.table_cell():
                        dpg.add_selectable(label=stat)
                    for col in range(1):
                        with dpg.table_cell():
                            dpg.add_selectable(label=champion_stats[stat])


def click_event_show_team_stats(sender, appdata):
    team_name = appdata[1]
    team_stats = jman.get_file_data(path_to_data_folder + "/teams.json")[team_name]
    for player in team_stats["Players"]:
        if dpg.does_alias_exist(team_name + ":" + player):
            dpg.remove_alias(team_name + ":" + player)

    with dpg.window(label=team_name + "'s Stats"):
        with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Winrate")
            dpg.add_table_column(label="Games Played")
            dpg.add_table_column(label="Games Won")
            dpg.add_table_column(label="Games Lost")
            for team_stat in range(1):
                with dpg.table_row():
                    for column in range(4):
                        team_winrate = round((team_stats["Games Won"] / team_stats["Games Played"]) * 100, 4)
                        if column == 0:
                            dpg.add_text(str(team_winrate) + "%")
                        if column == 1:
                            dpg.add_text(str(team_stats["Games Played"]))
                        if column == 2:
                            dpg.add_text(str(team_stats["Games Won"]))
                        if column == 3:
                            dpg.add_text(str(team_stats["Games Lost"]))
        dpg.add_text("------------------------")
        dpg.add_text("Players")
        dpg.add_text("------------------------")
        for player in team_stats["Players"]:
            dpg.add_text(player, tag=team_name + ":" + player)
            dpg.bind_item_handler_registry(team_name + ":" + player, player_filter_event_handler)


def show_player_champion_stats(player_name):
    champion_data = jman.get_file_data(path_to_data_folder + "/player_champion_data.json")[player_name]
    with dpg.window(label=player_name + "'s Champion's"):
        dpg.add_text(player_name + "'s Champion's Stats")
        dpg.add_text("------------------------------------------------")
        with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Champion")
            dpg.add_table_column(label="Winrate")
            dpg.add_table_column(label="KDA Ratio")
            dpg.add_table_column(label="Games Played")
            dpg.add_table_column(label="Games Won")
            dpg.add_table_column(label="Games Lost")
            for champion in champion_data:
                with dpg.table_row():
                    for column in range(7):
                        champion_winrate = round((champion_data[champion]["Games Won"] / champion_data[champion]["Games Played"]) * 100, 4)
                        if column == 0:
                            dpg.add_text(champion, tag=player_name + ":" + champion)
                            dpg.bind_item_handler_registry(player_name + ":" + champion, player_champion_event_handler)
                        if column == 1:
                            dpg.add_text(str(champion_winrate) + "%")
                        if column == 2:
                            dpg.add_text(str(champion_data[champion]["KDA Ratio"]))
                        if column == 3:
                            dpg.add_text(str(champion_data[champion]["Games Played"]))
                        if column == 4:
                            dpg.add_text(str(champion_data[champion]["Games Won"]))
                        if column == 5:
                            dpg.add_text(str(champion_data[champion]["Games Lost"]))


with dpg.item_handler_registry() as player_filter_event_handler:
    dpg.add_item_clicked_handler(callback=click_event_show_player_stats)

with dpg.item_handler_registry() as player_champion_event_handler:
    dpg.add_item_clicked_handler(callback=click_event_show_player_champion_stats)

with dpg.item_handler_registry() as team_filter_event_handler:
    dpg.add_item_clicked_handler(callback=click_event_show_team_stats)


def generate_player_filter():
    name_list = []
    player_stat_data = jman.get_file_data(path_to_data_folder + "/player_stats.json")
    window = dpg.add_window(label="Registered Players", on_close=dpg.delete_item)
    name_filter = dpg.add_input_text(label="Filter By Player Name or Team", parent=window, width=150, callback=lambda: filter_config(filter_set, dpg.get_value(name_filter)))
    with dpg.filter_set(parent=window) as filter_set:
        for name in player_stat_data:
            name_list.append(name)
            dpg.add_text(name, filter_key=name + player_stat_data[name]["Team"], tag="Player:" + name)
            dpg.bind_item_handler_registry("Player:" + name, player_filter_event_handler)


def generate_teams_filter():
    team_data = jman.get_file_data(path_to_data_folder + "/teams.json")
    window = dpg.add_window(label="Registered Teams", on_close=dpg.delete_item)
    team_filter = dpg.add_input_text(label="Filter By Team Name", parent=window, width=150, callback=lambda: filter_config(filter_set, dpg.get_value(team_filter)))
    with dpg.filter_set(parent=window) as filter_set:
        for team in team_data:
            dpg.add_text(team, filter_key=team, tag=team)
            dpg.bind_item_handler_registry(team, team_filter_event_handler)


def filter_config(filter_id, filter_string):
    dpg.set_value(filter_id, filter_string)


def remove_name_tags(name_list):
    for name in name_list:
        dpg.remove_alias(name)
