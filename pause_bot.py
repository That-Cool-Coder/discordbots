import os
import time

from better_profanity import profanity
profanity.load_censor_words()

from common import run_bot
from abstract_bot import Bot

class PauseBot(Bot):
    def __init__(self, token: str):
        super().__init__(token)

    async def on_message(self, message):
        if message.author != self.user:
            if profanity.censor(message.content) != message.content:
                await message.channel.send('pause bro')

if __name__ == '__main__':
    run_bot(PauseBot)