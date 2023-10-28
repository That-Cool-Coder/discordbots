import os
import random
import string
import time

from better_profanity import profanity
profanity.load_censor_words()

from common import run_bot
from abstract_bot import Bot

class PauseBot(Bot):
    # Stupid joke bot that says "Pause" if it detects anyone saying sexual things but only those involving men
    # (Friends seem to think it is funny)
    # Also has ability to "hate" a specific user - flagging them randomly with increasing probability over time
    ANTI_TRIGGER_WORDS = ['woman', 'female', 'girl', 'lady']
    TRIGGER_NOUNS = ['man', 'men', 'dad', 'boy', 'boys']
    TRIGGER_VERBS = ['like', 'love', 'adore', 'play', 'tickle', 'luv', 'kiss', 'smooch', 'hug', 'heart']

    def __init__(self, token: str, username_to_hate: str = ''):
        super().__init__(token)
        self.username_to_hate = username_to_hate

        self.hate_message_count = 0

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        if any([word in message.content for word in self.ANTI_TRIGGER_WORDS]):
            return

        should_send = False

        words = message.content.lower().translate(str.maketrans("","", string.punctuation)).split(' ')
        if any([word in self.TRIGGER_NOUNS for word in words]):
            if profanity.contains_profanity(message.content) or any([word in self.TRIGGER_VERBS for word in words]):
                should_send = True
        
        if message.author.name == self.username_to_hate:
            self.hate_message_count += 1
            if random.random() < self.calc_chance_of_hating():
                should_send = True
        
        if should_send:
            await message.channel.send(':pause_button:   Pause bro')
    
    def calc_chance_of_hating(self):
        return (1 - 1/(2**(self.hate_message_count / 20))) * 0.5

if __name__ == '__main__':
    run_bot(PauseBot, {hate_user: bool, username: str})