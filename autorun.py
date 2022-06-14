import json
import time
from json.decoder import JSONDecodeError
import subprocess
import threading
import sys

from common import *

CONF_FILE_NAME = 'autorun_conf.json'

BOT_FILES = {
    'BotBot' : 'botbot.py',
    'CounterBot' : 'counter_bot.py',
    'ImageScraperBot' : 'image_scraper_bot.py',
    'BruhBot' : 'bruh_bot.py',
    'SpamBot' : 'spam_bot.py',
    'PauseBot' : 'pause_bot.py'
}

def show_config_error(message: str):
    print(f'Error reading config file: {message}')
    input('Press enter to quit')
    quit()

file = None
try:
    file = open(CONF_FILE_NAME)
    config = json.loads(file.read())
except FileNotFoundError:
    show_config_error(f'Cannot find config file ({CONF_FILE_NAME})')
except PermissionError:
    show_config_error(f'Insufficient permissions')
except JSONDecodeError:
    show_config_error('Cannot decode contents')
except:
    show_config_error('Unknown error')
finally:
    if file is not None:
        file.close()

def run_bot_in_subprocess(bot_name: str, bot_config: dict):
    print(f'Starting {bot_name}...')

    args = [sys.executable, BOT_FILES[bot_name], bot_config["token"]]
    for field in bot_config:
        if field == 'token' or field == 'active':
            continue
        args.append(f'{field}={bot_config[field]}')
    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    for bot_name in config:
        if config[bot_name]['active']:
            if bot_name not in BOT_FILES:
                show_config_error(f'Bot {bot_name} does not exist')
            run_bot_in_subprocess(bot_name, config[bot_name])

    while True:
        time.sleep(10)