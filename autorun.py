import json
import time
from json.decoder import JSONDecodeError
import subprocess
import threading
import sys
import copy
import asyncio
import atexit

from common import *

import botbot
import bruh_bot
import counter_bot
import dumbxp
import image_scraper_bot
import pause_bot

CONF_FILE_NAME = 'autorun_conf.json'

BOT_CLASSES = {
    'BotBot' : botbot.BotBot,
    'BruhBot' : bruh_bot.BruhBot,
    'CounterBot' : counter_bot.CounterBot,
    'DumbXp' : dumbxp.DumbXp, 
    'ImageScraperBot' : image_scraper_bot.ImageScraperBot,
    'PauseBot' : pause_bot.PauseBot,
}

def show_config_error(message: str):
    print(f'Error reading config file: {message}')
    input('Press enter to quit')
    quit()

file = None
try:
    file = open(CONF_FILE_NAME)
    config = json.load(file)
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

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    for bot_name in config:
        if config[bot_name]['active']:
            if bot_name not in BOT_CLASSES:
                show_config_error(f'Bot {bot_name} does not exist')
                continue

            print(f'Starting {bot_name}')
            bot_config = copy.deepcopy(config[bot_name])
            del bot_config['active']

            instance = None
            try:
                instance = BOT_CLASSES[bot_name](**bot_config)
                event_loop.create_task(instance.start())
                atexit.register(instance.cleanup)
            except Exception as e:
                print('Error running bot - token or configuration is probably invalid')
                if instance is not None:
                    instance.cleanup()
                print(e)
                
    event_loop.run_forever()