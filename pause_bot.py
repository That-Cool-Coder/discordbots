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
    ANTI_CENSOR_WORDS = ['woman', 'female', 'girl', 'lady']
    EXTRA_CENSOR_NOUNS = ['man', 'men', 'guy', 'guys', 'dad']
    EXTRA_CENSOR_VERBS = ['like', 'love', 'adore', 'play', 'tickle', 'luv', 'kiss', 'smooch', 'hug']

    def __init__(self, token: str):
        super().__init__(token)

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if message.author != self.user:
            if not any([word in message.content for word in self.ANTI_CENSOR_WORDS]):
                triggered = False
                if profanity.contains_profanity(message.content):
                    triggered = True
                else:
                    words = message.content.lower().translate(str.maketrans("","", string.punctuation)).split(' ')
                    if any([word in self.EXTRA_CENSOR_NOUNS for word in words]) and any([word in self.EXTRA_CENSOR_VERBS for word in words]):
                        triggered = True
                if triggered:
                    await message.channel.send(':pause_button:   Pause bro')

if __name__ == '__main__':
    run_bot(PauseBot)