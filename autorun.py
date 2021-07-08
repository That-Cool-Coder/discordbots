import json
from json.decoder import JSONDecodeError
import subprocess
import sys

from botbot import *
from counter_bot import *
from common import *

CONF_FILE_NAME = 'conf.json'

BOTS = {
    'BotBot' : 'botbot.py',
    'CounterBot' : 'counter_bot.py'
}

def show_config_error(message: str):
    print(f'Error reading config file: {message}')
    input('Press enter to quit')
    quit()

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
    file.close()

if __name__ == '__main__':
    for bot_name in config:
        if config[bot_name]['active']:
            if bot_name not in BOTS:
                show_config_error(f'Bot {bot_name} does not exist')
            subprocess.Popen(
                [sys.executable, BOTS[bot_name], config[bot_name]['token']],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        pass