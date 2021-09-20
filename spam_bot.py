import os
import time

from common import run_bot
from abstract_bot import Bot

class SpamBot(Bot):
    '''You'll find that a lot of the 'consts' in this class
    are actually defined in the on_ready() method,
    as they rely upon data that is only available after login
    '''

    spamming = False
    STOP_TRIGGER = 'stop'

    def __init__(self, token: str, interval: float):
        super().__init__(token)
        self.interval = interval
    
    async def on_ready(self):
        self.RESPONSE_TRIGGER = f'hey {self.user.name.lower()}'

    async def on_message(self, message):
        if message.author != self.user:
            if message.content.lower().startswith(self.RESPONSE_TRIGGER):
                cleaned_message = message.content[len(self.RESPONSE_TRIGGER):].strip()
                if cleaned_message.lower().startswith(self.STOP_TRIGGER.lower()):
                    self.spamming = False
                elif cleaned_message != '':
                    self.spamming = True
                    await self.spam(message.channel, cleaned_message)
    
    async def spam(self, channel, text):
        if self.spamming:
            await channel.send(text)
            time.sleep(self.interval)
            await self.spam(channel, text)

if __name__ == '__main__':
    run_bot(SpamBot, {'interval': float})