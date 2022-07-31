import modules.json_manager as jman
import modules.data_location_preferences as dlp
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from os.path import abspath

pdfmetrics.registerFont(TTFont('OpenSans', 'Fonts/OpenSans-Regular.ttf'))


def export_general_stats_pdf():
    relative_path = dlp.path_to_data_folder() + "/Exports/General_Stats.pdf"

    c = Canvas(filename=relative_path, pagesize=letter)

    width, height = c._pagesize

    teams = list(jman.get_file_data(dlp.path_to_data_folder() + "/teams.json"))
    accepted_player_stats = ["Winrate", "KDA Ratio", "Kills", "Deaths", "Assists"]

    c.drawCentredString(width / 2, (height / 2) + 190, text="General Team/Player Stat Data")
    c.setFontSize(10)
    c.drawCentredString(width / 2, (height / 2) + 150, text="(Made using League of Stats)")

    c.showPage()

    for team in teams:
        c.setFont('OpenSans', 30)
        c.drawCentredString(width / 2, 700, team)
        team_stat_table(team, c, (width / 2) - 125, 635)

        c.setFontSize(15)
        c.drawCentredString(width / 2, 500, team + "'s Players")
        team_player_stat_table(team, c, (width / 2) - 140, 350, accepted_player_stats)
        c.showPage()
    print("General Stats exported to\n\t" +
          abspath(relative_path))
    c.save()


def team_player_stat_table(team_name, canvas, x, y, accepted_stats):
    data = jman.team_player_stats_to_tuple(accepted_stats, team_name)
    table_data = [["Player Name"]]
    for tracked_stat in accepted_stats:
        table_data[0].append(tracked_stat)

    for player in list(data):
        table_data.append(data[player][1])

    all_cells = [(0, 0), (-1, -1)]
    header = [(0, 0), (-1, 0)]
    column0 = [(0, 0), (0, -1)]
    column1 = [(1, 0), (1, -1)]
    column2 = [(2, 0), (2, -1)]
    column3 = [(3, 0), (3, -1)]
    column4 = [(4, 0), (4, -1)]
    column5 = [(5, 0), (5, -1)]
    table_style = TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        # ("VALIGN", all_cells[0], all_cells[1], "TOP"),
        ("LINEBELOW", header[0], header[1], 1, colors.deeppink),
        ("ALIGN", column0[0], column0[1], "CENTER"),
        ("ALIGN", column1[0], column1[1], "CENTER"),
        ("ALIGN", column2[0], column2[1], "CENTER"),
        ("ALIGN", column3[0], column3[1], "CENTER"),
        ("ALIGN", column4[0], column4[1], "CENTER"),
        ("ALIGN", column5[0], column5[1], "CENTER")
    ])

    t = Table(table_data)
    t.setStyle(table_style)
    t.wrapOn(canvas, x, y)
    t.drawOn(canvas, x, y)


def team_stat_table(team_name, canvas, x, y):
    team_stats = ["Winrate", "Games Won", "Games Played", "Games Lost"]
    data = jman.team_stats_to_tuple(team_stats, team_name)[team_name]

    header = [(0, 0), (-1, 0)]
    column0 = [(0, 0), (0, -1)]
    column1 = [(1, 0), (1, -1)]
    column2 = [(2, 0), (2, -1)]
    column3 = [(3, 0), (3, -1)]

    table_style = TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        # ("VALIGN", all_cells[0], all_cells[1], "TOP"),
        ("LINEBELOW", header[0], header[1], 1, colors.black),
        ("ALIGN", column0[0], column0[1], "CENTER"),
        ("ALIGN", column1[0], column1[1], "CENTER"),
        ("ALIGN", column2[0], column2[1], "CENTER"),
        ("ALIGN", column3[0], column3[1], "CENTER")
    ])

    t = Table(data)
    t.setStyle(table_style)
    t.wrapOn(canvas, 0, 0)
    t.drawOn(canvas, x, y)


def export_player_stats(player_name):
    relative_path = dlp.path_to_data_folder() + "/Exports/" + player_name + "_Stats.pdf"
    c = Canvas(filename=relative_path, pagesize=letter)
    width, height = c._pagesize

    data = player_champion_data(player_name)

    player_table(player_name, data[player_name], c, 230, 400)
    champion_data = {key: value for key, value in data.items() if key != player_name}
    player_champion_table(champion_data, c, 230, 200)
    print(f"{player_name}'s Stats exported to:\n\t" +
          abspath(relative_path))
    c.save()


def player_champion_data(player_name):
    player_stats = ["Games Won", "Games Lost", "Games Played", "Winrate", "KDA Ratio", "Kills", "Deaths", "Assists", "Average CS", "Overall CS", "Average Gold Collected",
                    "Overall Gold Collected"]

    champion_stats = ["Games Played", "Games Won", "Games Lost", "Total Kills", "Total Deaths", "Total Assists", "Total CS", "Total Gold", "KDA Ratio"]
    data = jman.player_champion_stats_to_tuple(player_name, player_stats, champion_stats)
    return data
    # Returns:
    # {'Player Name' : (('Stat 1', 'Stat 2', 'Stat 3', ...), (Stat 1 Value, Stat 2 Val, Stat 3 Val, ...)),
    # 'Champion 1 Name: (('Stat 1', 'Stat 2', 'Stat 3', ...), (Stat 1 Value, Stat 2 Val, Stat 3 Val, ...)),
    # 'Champion 2 Name: ((...)),
    #  ... }


def player_table(player_name, data: list or tuple, canvas, x, y):
    # data must be of the form
    # (("Stat 1", "Stat 2", "Stat 3", ...), ("Stat 1 Value", "Stat 2 Value", "Stat 3 Value", ...))
    # or
    # [["Stat 1", "Stat 2", "Stat 3", ...], , ["Stat 1 Value", "Stat 2 Value", "Stat 3 Value", ...]]

    modified_data = []

    # Modifies Data to the Form:
    # [["Stat 1", "Stat 1 Value"], ["Stat 2", "Stat 2 Value"], ...]
    for index in range(len(data[0])):
        modified_data.append([])
        modified_data[index].append(data[0][index])
        modified_data[index].append(data[1][index])

    table_style = TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        # ("VALIGN", all_cells[0], all_cells[1], "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
        ("ALIGN", (2, 0), (2, -1), "RIGHT")
    ])
    t = Table(modified_data)
    t.setStyle(table_style)
    t.wrapOn(canvas, 0, 0)
    t.drawOn(canvas, x, y)
    canvas.drawCentredString(x + 92, y + 245, player_name + "'s Stats")


def player_champion_table(data: dict, canvas, x, y):
    # data must be of the form
    # {"Champion 1" : (("Stat 1", "Stat 2", "Stat 3", ...), ("Stat 1 Value", "Stat 2 Value", "Stat 3 Value", ...)),
    #  "Champion 2" : (("Stat 1", "Stat 2", "Stat 3", ...), ("Stat 1 Value", "Stat 2 Value", "Stat 3 Value", ...)),
    #   ... }

    table_style = TableStyle([
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        # ("VALIGN", all_cells[0], all_cells[1], "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
        ("ALIGN", (2, 0), (2, -1), "RIGHT")
    ])

    for champion in list(data):
        canvas.showPage()
        modified_data = []
        for index in range(len(data[champion][0])):
            modified_data.append([])
            modified_data[index].append(data[champion][0][index])
            modified_data[index].append(data[champion][1][index])
        t = Table(modified_data)
        t.setStyle(table_style)
        t.wrapOn(canvas, 0, 0)
        t.drawOn(canvas, x, y)
        if champion == "":
            champion = "[No Name Found]"
        canvas.drawCentredString(x + 70, y + 245, "Stats for " + champion)
