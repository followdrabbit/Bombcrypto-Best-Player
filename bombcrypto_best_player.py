# -*- coding: utf-8 -*-    
import argparse
import mss
import numpy as np
import pyautogui
import sys
import time
import yaml
from cv2 import cv2
from os import listdir
from random import randint
from random import random
from random import seed


parser = argparse.ArgumentParser(description="ALL ARGUMENTS ARE OPTIONAL!")
parser.add_argument("--save-logs",
                    action=argparse.BooleanOptionalAction,
                    help="If set, save logs to a file.",)
parser.add_argument("--logs-name",
                    help="Use to change logs filename (default: bcoin_collector.log).s",
                    default="bcoin_collector.log")
parser.add_argument("--logs-path",
                    help="Use to change logs file path (default: ./logs/).",
                    default="./logs/")
args = parser.parse_args()
config = vars(args)


print(r'=========================================================================================================')
print(r'| __   __         __   __   __       __  ___  __      __   ___  __  ___     __                 ___  __  |')
print(r'||__) /  \  |\/| |__) /  ` |__) \ / |__)  |  /  \    |__) |__  /__`  |     |__) |     /\  \ / |__  |__) |')
print(r'||__) \__/  |  | |__) \__, |  \  |  |     |  \__/    |__) |___ .__/  |     |    |___ /~~\  |  |___ |  \ |')
print(r'|                                                                                                       |')
print(r'=========================================================================================================')
print(r'|                                                                                                       |')
print(r'|                 Press   "ctrl + c" to interrupt Bombcrypto Best Player execution                      |')
print(r'|                                                                                                       |')
print(r'=========================================================================================================')


def logger(message):
    formatted_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    formatted_message = "[{}] => {}".format(formatted_datetime, message)
    print(formatted_message)

    if config['save_logs']:
        logger_file = open(config['logs_path'] + config['logs_name'], "a", encoding='utf-8')
        logger_file.write(formatted_message + '\n')
        logger_file.close()

    return True


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def load_images(dir_path='./targets/'):
    """ Programmatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def add_randomness(n, random_n_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        random_n_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if random_n_factor_size is None:
        randomness_percentage = 0.1
        random_n_factor_size = randomness_percentage * n

    random_factor = 2 * random() * random_n_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - random_n_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)


def move_to_with_randomness(x, y, t):
    pyautogui.moveTo(add_randomness(x, 10), add_randomness(y, 10), t+random()/2)


def click_btn(img, timeout=5, threshold=0.7):
    start = time.time()
    has_timed_out = False
    while not has_timed_out:
        matches = positions(img, threshold=threshold)

        if len(matches) == 0:
            has_timed_out = time.time()-start > timeout
            continue

        x, y, w, h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        move_to_with_randomness(pos_click_x, pos_click_y, 1)
        pyautogui.click()
        return True

    return False


def print_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:, :, :3]


def positions(target, threshold=0.7, img=None):
    if img is None:
        img = print_screen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    y_location, x_location = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(x_location, y_location):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def check_img(img, timeout=3, threshold=0.7):
    start = time.time()
    has_timed_out = False
    while not has_timed_out:
        matches = positions(img, threshold=threshold)

        if len(matches) == 0:
            has_timed_out = time.time()-start > timeout
            continue

        return True


def scroll():
    pipe_bars = positions(images['pipe_bar'], threshold=0.8)
    if len(pipe_bars) == 0:
        return

    x, y, w, h = pipe_bars[len(pipe_bars)-1]
    move_to_with_randomness(x, y, 1)
    pyautogui.dragRel(0, -200, duration=1, button='left')


def refresh_heroes_positions():
    logger('Refreshing heroes positions')
    global attempt_count
    click_btn(images['go_back_arrow'])
    if click_btn(images['treasure_hunt_icon']):
        attempt_count = 0
    else:
        logger('Refresh failed - Treasure hunt icon not found')
        attempt_count += 1


def send_heroes_to_work():
    logger('Looking for heroes to work')
    global attempt_count
    click_btn(images['go_back_arrow'])
    time.sleep(3)
    if click_btn(images['hero_icon']):
        attempt_count = 0
        time.sleep(randint(1, 5))
        offset = 140
        scroll_count = 0
        workers_send_count = 0

        while scroll_count < 6:
            scroll_count += 1
            green_bars = positions(images['green_bar'], threshold=0.9)
            for (x, y, w, h) in green_bars:
                move_to_with_randomness(x+offset+(w/2), y+(h/2), 1)
                pyautogui.click()
                workers_send_count += 1
            scroll()
            time.sleep(2)

        click_btn(images['x'])
        click_btn(images['treasure_hunt_icon'])

        if workers_send_count > 1:
            send_heroes_timer = randint(60, 180)
            logger('Heroes sent to work'.format(workers_send_count))
            logger('Cool down activated for {} seconds'.format(send_heroes_timer))
            time.sleep(send_heroes_timer)
        else:
            logger('No heroes available to work')
    else:
        logger('Unsuccessful search - Hero icon not found')
        attempt_count += 1


def coin_view():
    logger('Trying to check the amount of coins collected')
    global attempt_count
    if click_btn(images['chest']):
        logger('Check succeed')
        attempt_count = 0
        time.sleep(randint(3, 12))
        click_btn(images['x'])
        time.sleep(randint(1, 60))
        coin_view_timer = randint(60, 120)
        logger('Cool down activated for {} seconds'.format(coin_view_timer))
        time.sleep(coin_view_timer)
    else:
        logger('Check not succeed - Chest icon not found')
        attempt_count += 1


# Global variables
images = load_images()
attempt_count = 0


def login():
    logger('Trying to log in')
    global attempt_count
    if click_btn(images['connect'], timeout=15):
        if click_btn(images['connect_metamask'], timeout=15):
            if click_btn(images['login_en_us'], timeout=15):
                if check_img(images['treasure_hunt_icon'], timeout=15):
                    logger('Log in successfully')
                    attempt_count = 0
                    send_heroes_to_work()
                else:
                    logger('Log in failed - Treasure hunt icon not found')
                    attempt_count += 1
            else:
                logger('Log in failed - Login button not found')
                attempt_count += 1
        else:
            logger('Log in failed - Metamask connect button not found')
            attempt_count += 1
    else:
        logger('Log in failed - Connect button not found    ')
        attempt_count += 1
        pass


def errors_check():
    logger('Attempt counter > 10')
    global attempt_count

    if click_btn(images['error'], timeout=10):
        logger('Error message found - Trying to reload the page')
        pyautogui.hotkey('ctrl', 'f5')
        if check_img(images['connect'], timeout=15):
            logger('Page reloaded successfully')
            time.sleep(randint(13, 35))
            login()
            return
    else:
        logger('Trying to reload the page')
        click_btn(images['server_tag'], timeout=10)
        pyautogui.hotkey('ctrl', 'f5')
        if check_img(images['connect'], timeout=15):
            logger('Page reloaded successfully')
            time.sleep(randint(13, 35))
            login()
            return
        else:
            logger('Failed to reload page')


def main():
    login()

    while True:
        seed()
        random_number = (randint(0, 9))

        if attempt_count > 10:
            errors_check()
        elif 6 <= random_number < 11:
            send_heroes_to_work()
        elif 1 < random_number < 6:
            coin_view()
        else:
            refresh_heroes_positions()

        sys.stdout.flush()
        time.sleep(randint(3, 18))


if __name__ == '__main__':
    main()
