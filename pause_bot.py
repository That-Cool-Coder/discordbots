import os
import string
import time

from better_profanity import profanity
profanity.load_censor_words()

from common import run_bot
from abstract_bot import Bot

class PauseBot(Bot):
    # Stupid joke bot that says "Pause" if it detects anyone saying sexual things but only those involving men
    # (Friends seem to think it is funny)
    ANTI_TRIGGER_WORDS = ['woman', 'female', 'girl', 'lady']
    TRIGGER_NOUNS = ['man', 'men', 'dad', 'boy', 'boys']
    TRIGGER_VERBS = ['like', 'love', 'adore', 'play', 'tickle', 'luv', 'kiss', 'smooch', 'hug', 'heart']

    def __init__(self, token: str):
        super().__init__(token)

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        if any([word in message.content for word in self.ANTI_TRIGGER_WORDS]):
            return

        words = message.content.lower().translate(str.maketrans("","", string.punctuation)).split(' ')
        if any([word in self.TRIGGER_NOUNS for word in words]):
            if profanity.contains_profanity(message.content) or any([word in self.TRIGGER_VERBS for word in words]):
                await message.channel.send(':pause_button:   Pause bro')

if __name__ == '__main__':
    run_bot(PauseBot)