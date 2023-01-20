import random
import time

import discord

from common import run_bot
from abstract_bot import Bot

class CounterBot(Bot):
    '''A bot that counts up.
    If the previous post is an integer, add one and post that.
    Also has spam feature'''

    def __init__(self, token: str, reply_probability: float = 1, only_check_first_word: bool = True,
    global_spam_enabled: bool = False, whitelist_active: bool = False, spam_interval: float = 1, config_password: str = ''):
        super().__init__(token)
        self.reply_probability = reply_probability
        self.only_check_first_word = only_check_first_word # makes it count if you say "1094 test" for instance
        
        self.spam_interval = spam_interval
        self.global_spam_enabled = global_spam_enabled
        self.spam_enabled = self.global_spam_enabled
        self.whitelist_active = whitelist_active
        self.config_password = config_password
        self.whitelist = [] # if whitelist active only the people on this dict can use it
        self.blacklist = [] # people in here cannot use it
        self.admin_users = [] # people in here can change the conf

        self.spamming = False

        self.custom_response_trigger = None
    
    async def on_ready(self):
        self.DEFAULT_RESPONSE_TRIGGER = f'hey {self.user.name.lower()}'
    
    @property
    def response_trigger(self):
        return self.custom_response_trigger or self.DEFAULT_RESPONSE_TRIGGER

    async def on_message(self, message):
        # Don't reply to self
        if message.author != self.user:
            # Have a certain chance of replying
            if random.uniform(0, 1) < self.reply_probability:
                if self.only_check_first_word:
                    items = message.content.strip().split(' ')
                    text = items[0] if items else '-'
                else:
                    text = message.content

                # Only proceed if message is integer (ie only digits)
                if text.isdigit():
                    await message.channel.send(int(text) + 1)
                
            if message.content.lower().startswith(self.response_trigger) and self.global_spam_enabled:
                cleaned_message = message.content[len(self.response_trigger):].strip()
                try:
                    await self.start_process_response(cleaned_message, message.channel, message.author)
                except Exception:
                    pass
    
    async def start_process_response(self, cleaned_message: str, message_channel, message_author: discord.User):
        if cleaned_message.startswith('conf'):
            await self.start_config(cleaned_message.removeprefix('conf').strip(), message_channel, message_author)
        else:
            await self.maybe_start_spam(cleaned_message, message_channel, message_author)
    
    async def start_config(self, cleaned_message: str, message_channel, message_author: discord.User):

        async def ok():
            await message_channel.send('Done')
    
        # Priliminary match statement to make users admins
        # (match easier than if)
        match cleaned_message.split():
            case ['admin', *password_sections]:
                password = ' '.join(password_sections)
                if password == self.config_password:
                    self.admin_users.append(message_author.id)
                    await ok()

        if not message_author.id in self.admin_users:
            return

        match cleaned_message.split():
            case ['check']:
                await message_channel.send('Hi, you are admin')

            case ['on']:
                self.spam_enabled = True
                await ok()
            case ['off']:
                self.spam_enabled = False
                await ok()
                
            case ['list', 'white', 'on']:
                self.whitelist_active = True
                await ok()
            case ['list', 'white', 'off']:
                self.whitelist_active = False
                await ok()

            case ['list', list_name, *rest]:
                list_lookup = {'white' : self.whitelist, 'black' : self.blacklist}
                if list_name not in list_lookup:
                    return
                target_list = list_lookup[list_name]

                match rest:
                    case ['add', *sections]:
                        names = ' '.join(sections).split('|')
                        for name in names:
                            target_list += names
                        await ok()
                    case ['del', *sections]:
                        names = ' '.join(sections).split('|')
                        for name in names:
                            target_list.remove(name)
                        await ok()
                    case ['show']:
                        names = '\n'.join(['- ' + name for name in target_list])
                        await message_channel.send(f'Users in {list_name}list:\n{names}')
                    case ['clear']:
                        target_list = []
                        await ok()
            
            case ['interval', new_interval]:
                try:
                    self.spam_interval = float(new_interval)
                    ok()
                except ValueError:
                    pass
            
            case ['trigger', 'reset']:
                self.custom_response_trigger = None
                await ok()
            case ['trigger', 'set', *new_trigger]:
                self.custom_response_trigger = ' '.join(new_trigger)
                await ok()
    
    async def maybe_start_spam(self, cleaned_message, message_channel, message_author: discord.User):
        if not self.spam_enabled:
            return

        username = message_author.name
        
        if username in self.blacklist:
            return
        
        if self.whitelist_active and username not in self.whitelist:
            return

        if cleaned_message == 'stop':
            self.spamming = False
            return

        self.spamming = True
        await self.spam(cleaned_message, message_channel) 

    async def spam(self, text: str, message_channel):
        if self.spamming and self.spam_enabled:
            await message_channel.send(text)
            time.sleep(self.spam_interval)
            await self.spam(text, message_channel)

if __name__ == '__main__':
    run_bot(CounterBot, {'reply_probability':float, 'only_check_first_word': bool, 'global_spam_enabled': bool, 'spam_interval': float, 'whitelist_active': bool, 'spam_interval': float, 'config_password':str})