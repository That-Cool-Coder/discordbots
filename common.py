def get_bot_token():
    '''Get a bot token from the user to stop people hard-coding them,
    which is a security risk.
    Find the token under the bot's username in the bot tab of the application
    '''
    return input('Paste the bot token here and press enter: ')

def run_bot(bot_class, *args, **kwargs):
    '''Create a new bot of bot_class and run it
    Any arguments following bot_class will be passed to __init__'''
    try:
        bot_class(get_bot_token(), *args, **kwargs).run()
    except:
        raise
        print('Error running bot - token is probably invalid')