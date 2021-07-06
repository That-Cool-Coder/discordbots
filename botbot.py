import os
from common import run_bot
from abstract_bot import AbstractBot

class BotBot(AbstractBot):
    '''You'll find that a lot of the 'consts' in this class
    are actually defined in the on_ready() method,
    as they rely upon data that is only available after login
    '''

    CHATBOT_RUNNER_FILE = 'node_chatbot/chatbotRunner.mjs'
    is_activated = True
    requires_trigger = True
    
    def on_ready(self):
        print('hi')
        self.RESPONSE_TRIGGER = f'hey {self.user.name}'
        self.CONFIG_KEYWORD = f'${self.user.name}config'
        self.CONFIG_HELP = f'''```
usage: {self.CONFIG_KEYWORD} <argument>
arguments:
activate            allow the bot to talk
deactivate          prevent the bot from talking
require_trigger     only reply when addressed with "{self.RESPONSE_TRIGGER}"
no_require_trigger  reply to all messages in the channel
```'''

    def on_message(self, message):
        if message.author != self.user:
            reply = None

            if message.content.startswith(self.CONFIG_KEYWORD):
                reply = self.process_config_command(
                    message.content[len(self.CONFIG_KEYWORD):])
            
            elif self.is_activated:
                response_trigger_present = False
                clean_content = message.content
                if message.content.lower().startswith(self.RESPONSE_TRIGGER):
                    response_trigger_present = True
                    clean_content = message.content[len(self.RESPONSE_TRIGGER):]
                
                if (not self.requires_trigger) or response_trigger_present:
                    reply = self.create_reply(clean_content)

            if reply is not None:
                self.reply_to_message(message, reply)
        
    def create_reply(self, prompt: str):
        command = f'node {self.CHATBOT_RUNNER_FILE} {self.user.name} {prompt}'
        return os.popen(command).read()
    
    def process_config_command(self, command: str):
        '''Note that command should have no prefix like $config'''
        sections = command.split(' ')
        if 'activate' in sections:
            self.is_activated = True
            return 'I am activated'
        elif 'deactivate' in sections:
            self.is_activated = False
            return 'I am deactivated'
        elif 'require_trigger' in sections:
            self.requires_trigger = True
            return f'I will now only respond to messages starting with "{self.RESPONSE_TRIGGER}"'
        elif 'no_require_trigger' in sections:
            self.requires_trigger = False
            return 'I will now respond to all messages'
        elif 'help' in sections:
            return self.CONFIG_HELP
        else:
            return f'Unrecognised command. Type `{self.CONFIG_KEYWORD} help` for more info.'

if __name__ == '__main__':
    run_bot(BotBot)