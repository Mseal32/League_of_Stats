# import pytesseract
import cv2
import os
import modules.data_location_preferences as dl

player_one_y = 255
player_two_y = 305
player_three_y = 355
player_four_y = 405
player_five_y = 455
player_six_y = 585
player_seven_y = 635
player_eight_y = 685
player_nine_y = 735
player_ten_y = 785

y_coord_list = [player_one_y, player_two_y, player_three_y, player_four_y, player_five_y, player_six_y, player_seven_y, player_eight_y, player_nine_y, player_ten_y]

path_to_data_folder = dl.path_to_data_folder()


def read_image(img):
    pytesseract.pytesseract.tesseract_cmd = r"modules/Tesseract-OCR/tesseract.exe"
    image = cv2.imread(img, 0)
    height = image.shape[0]
    dim = (1577, height)
    image = cv2.resize(image, dim)
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    players = {
        "Player1": read_player_one(thresh),
        "Player2": read_player_two(thresh),
        "Player3": read_player_three(thresh),
        "Player4": read_player_four(thresh),
        "Player5": read_player_five(thresh),
        "Player6": read_player_six(thresh),
        "Player7": read_player_seven(thresh),
        "Player8": read_player_eight(thresh),
        "Player9": read_player_nine(thresh),
        "Player10": read_player_ten(thresh)
    }
    return players


def save_new_img(img, teams):
    image = cv2.imread(img)
    team1 = teams[0]
    team2 = teams[1]
    current_dir = os.getcwd()
    file_name = f"{team1}_VS_{team2}_{read_date(img)}.jpg"
    os.chdir(path_to_data_folder + "/Match_History")
    cv2.imwrite(file_name, image)
    os.chdir(current_dir)


def read_name(thresh, player_y_coord):
    x, y, w, h, = 205, player_y_coord, 270, 60
    ROI = thresh[y:y + h, x:x + w]
    data = pytesseract.image_to_string(ROI, config='--psm 6')
    data = data[1::]
    data = data.strip()
    return data


def read_kda(thresh, player_y_coord):
    x, y, w, h, = 775, player_y_coord, 170, 60
    ROI = thresh[y:y + h, x:x + w]

    data = pytesseract.image_to_string(ROI, config='-c tessedit_char_whitelist=1234567890/ --psm 3')
    data = data.split('/')

    for num in range(len(data)):
        if "°" in data[num]:
            data[num] = data[num].replace("°", "")
        data[num] = data[num].strip()
    return data


def read_cs(thresh, player_y_coord):
    x, y, w, h, = 965, player_y_coord, 125, 60
    ROI = thresh[y:y + h, x:x + w]
    data = pytesseract.image_to_string(ROI, config='lang=eng' '--psm 6')
    data = data.strip()
    return data


def read_gold(thresh, player_y_coord):
    x, y, w, h, = 1065, player_y_coord, 125, 60
    ROI = thresh[y:y + h, x:x + w]
    data = pytesseract.image_to_string(ROI, config='--psm 6')
    data = data.strip()
    return data


def read_player_one(thresh):
    name = read_name(thresh, player_one_y)
    kda = read_kda(thresh, player_one_y)
    cs = read_cs(thresh, player_one_y)
    gold = read_gold(thresh, player_one_y)
    return [name, kda, cs, gold]


def read_player_two(img):
    name = read_name(img, player_two_y)
    kda = read_kda(img, player_two_y)
    cs = read_cs(img, player_two_y)
    gold = read_gold(img, player_two_y)
    return [name, kda, cs, gold]


def read_player_three(img):
    name = read_name(img, player_three_y)
    kda = read_kda(img, player_three_y)
    cs = read_cs(img, player_three_y)
    gold = read_gold(img, player_three_y)
    return [name, kda, cs, gold]


def read_player_four(img):
    name = read_name(img, player_four_y)
    kda = read_kda(img, player_four_y)
    cs = read_cs(img, player_four_y)
    gold = read_gold(img, player_four_y)
    return [name, kda, cs, gold]


def read_player_five(img):
    name = read_name(img, player_five_y)
    kda = read_kda(img, player_five_y)
    cs = read_cs(img, player_five_y)
    gold = read_gold(img, player_five_y)
    return [name, kda, cs, gold]


def read_player_six(img):
    name = read_name(img, player_six_y)
    kda = read_kda(img, player_six_y)
    cs = read_cs(img, player_six_y)
    gold = read_gold(img, player_six_y)
    return [name, kda, cs, gold]


def read_player_seven(img):
    name = read_name(img, player_seven_y)
    kda = read_kda(img, player_seven_y)
    cs = read_cs(img, player_seven_y)
    gold = read_gold(img, player_seven_y)
    return [name, kda, cs, gold]


def read_player_eight(img):
    name = read_name(img, player_eight_y)
    kda = read_kda(img, player_eight_y)
    cs = read_cs(img, player_eight_y)
    gold = read_gold(img, player_eight_y)
    return [name, kda, cs, gold]


def read_player_nine(img):
    name = read_name(img, player_nine_y)
    kda = read_kda(img, player_nine_y)
    cs = read_cs(img, player_nine_y)
    gold = read_gold(img, player_nine_y)
    return [name, kda, cs, gold]


def read_player_ten(img):
    name = read_name(img, player_ten_y)
    kda = read_kda(img, player_ten_y)
    cs = read_cs(img, player_ten_y)
    gold = read_gold(img, player_ten_y)
    return [name, kda, cs, gold]


def read_date(img):
    pytesseract.pytesseract.tesseract_cmd = r"modules/Tesseract-OCR/tesseract.exe"
    image = cv2.imread(img, 0)
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    x, y, w, h, = 475, 60, 170, 60
    ROI = thresh[y:y + h, x:x + w]
    data = pytesseract.image_to_string(ROI, config='--psm 6')
    new_data = data.replace("/", "_")
    new_data = new_data.rstrip()
    return new_data
