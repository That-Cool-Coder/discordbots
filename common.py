def get_bot_token():
    '''Get a bot token from the user to stop people hard-coding them,
    which is a security risk.
    Find the token under the bot's username in the bot tab of the application
    '''
    return input('Paste the bot token here and press enter: ')

def run_bot(bot_class):
    try:
        bot_class(get_bot_token()).run()
    except:
        print('Error running bot - token is probably invalid')