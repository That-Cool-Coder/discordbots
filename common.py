import sys

def run_bot(bot_class, required_conf_fields={}):
    '''Create a new bot of bot_class and run it'''
    try:
        token, conf = get_bot_token_and_conf(required_conf_fields)
        bot_class(token, **conf).run()
    except:
        raise
        print('Error running bot - token is probably invalid')

def get_bot_token_and_conf(required_conf_fields=[]):
    '''Try to get configuration for the bot from argv.
    If there is no argv then get it from input().
    configuration includes bot token and the things
    specified in require_fields

    required_conf_fields should be like so:
    {somevar: int, someothervar: str, somevarvar: float}

    argv format should be like so:
    python bot_file.py mytokenhere somevalue=123 othervalue=456
    '''
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
        conf = {}
        for arg_idx in range(2, len(sys.argv)):
            arg_var = sys.argv[arg_idx]
            field = arg_var.split('=', 1)[0]
            field_value = arg_var.split('=', 1)[1]
            if field not in required_conf_fields:
                raise RuntimeError(f'Unexpected command line argument: {field}')
            if required_conf_fields[field] == int:
                conf[field] = int(field_value)
            elif required_conf_fields[field] == float:
                conf[field] = float(field_value)
            elif required_conf_fields[field] == str:
                conf[field] = field_value
            else:
                raise RuntimeError(
                    f'Unsupported conf var type: {required_conf_fields[field]}')
    else:
        token = input('Paste the bot token here and press enter: ')
        conf = {}
        for field in required_conf_fields:
            field_value = input(f'Enter value of {field}: ')
            if required_conf_fields[field] == int:
                conf[field] = int(field_value)
            elif required_conf_fields[field] == float:
                conf[field] = float(field_value)
            elif required_conf_fields[field] == str:
                conf[field] = field_value
    
    return (token, conf)
