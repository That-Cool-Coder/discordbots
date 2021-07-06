import json
from json.decoder import JSONDecodeError
from multiprocessing import Process
from multiprocessing.process import parent_process

from botbot import *
from counter_bot import *
from common import *

CONF_FILE_NAME = 'conf.json'

BOTS = {
    'BotBot' : BotBot,
    'CounterBot' : CounterBot
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
            bot_arguments = config[bot_name].copy()
            del bot_arguments['active']
            del bot_arguments['token']
            bot = BOTS[bot_name](config[bot_name]['token'], **bot_arguments)
            p = Process(target=bot.run, daemon=True, )
            p.start()

    while True:
        pass