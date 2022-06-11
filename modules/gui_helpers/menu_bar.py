import dearpygui.dearpygui as dpg
from modules.gui_helpers import manual_entry
import modules.data_location_preferences as dl
import os


def show_file_dialog(sender, appdata):
    dpg.show_item("jpg_fileselector")


def team_read_setup(sender, appdata):
    manual_entry.main(appdata)


def manual_add_match_summary(sender, appdata):
    manual_entry.manual_entry_match_summary()


def los_license_info(sender, appdata):
    with dpg.window(label="League of Stats Software & License Information"):
        dpg.add_text("NOTICE: Any references to Software within this window refers to any and all directories, files, or any other forms of media\nthat were included within "
                     "the distribution of this project")
        dpg.add_separator()
        dpg.add_text("Like most other distributed software, League of Stats was created using a variety of tools.\n"
                     "In regards to these tools, I will give credit where credit is owed (and only slightly legally obligated to do so)\n"
                     "The heavy-hitters used to create this Software are as follows:")
        dpg.add_text("DearpyGui", bullet=True)
        dpg.add_text("Tesseract & Pytesseract", bullet=True)
        dpg.add_text("Opencv-Python", bullet=True)
        dpg.add_separator()
        dpg.add_text("If you have even a hint of Python knowledge, or are interested in development of your own,\n"
                     "be sure to check each of them out as they are LIFE SAVERS\n"
                     "More information and licenses for each of the Packages mentioned above can be found using the 'Legal' menu tab on the menu bar\n"
                     "and selecting 'Package Information & Licenses'\n\n"
                     "This Software itself is distributed under the MIT License. You can view the license by clicking on the button below,\n"
                     "which will open the LICENSE text file (found in the 'root' software directory) in Notepad")
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_text("                                              ")
            dpg.add_button(label="Open License", callback=lambda : os.system("notepad.exe LICENSE.TXT"))


def delete_all_data_window(sender, appdata):
    with dpg.window(no_title_bar=True, pos=[450, 300]):
        dpg.add_text("Are you sure you want to reset ALL saved stat data?", color=[180, 40, 15])
        dpg.add_text("     (This process can not be undone!)")
        dpg.add_text("   ")
        with dpg.group(horizontal=True):
            dpg.add_text("       ")
            dpg.add_button(label="Cancel", callback=cancel_delete_data)
            dpg.add_text("  ")
            dpg.add_button(label="Reset All Stat Data", callback=delete_all_data)


def cancel_delete_data(sender, appdata):
    dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(sender)))


def delete_all_data(sender, appdata):
    data_folder_path = dl.path_to_data_folder()
    with open(data_folder_path + "/player_stats.json", "w") as stat_file:
        stat_file.write("{}")
    with open(data_folder_path + "/player_champion_data.json", "w") as champion_data_file:
        champion_data_file.write("{}")
    with open(data_folder_path + "/teams.json", "w") as teams_file:
        teams_file.write("{}")
    dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(sender)))

def add_solo_player(sender, appdata):
    manual_entry.add_solo_player()