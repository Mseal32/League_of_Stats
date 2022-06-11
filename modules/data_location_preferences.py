import os


def path_to_data_folder():
    with open("Data_Location_Preferences.txt", 'r') as prefs_file:
        for line in prefs_file:
            if "=" not in line:
                continue
            line = line.strip()
            data = line.split("=")
            for string in range(len(data)):
                data[string] = data[string].strip()
            path_to_data_folder_str = data[1]
            break
    return path_to_data_folder_str
