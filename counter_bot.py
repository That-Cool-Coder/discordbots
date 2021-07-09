import random
from common import run_bot
from abstract_bot import AbstractBot

class CounterBot(AbstractBot):
    '''A bot that counts up.
    If the previous post is an integer, add one and post that'''

    def __init__(self, token: str, reply_probability=1):
        super().__init__(token)
        self.reply_probability = reply_probability

    async def on_message(self, message):
        # Don't reply to self
        if message.author != self.user:
            # Have a certain chance of replying
            if random.uniform(0, 1) < self.reply_probability:
                # Only proceed if message is integer (ie only digits)
                if message.content.isdigit():
                    await message.channel.send(int(message.content) + 1)

if __name__ == '__main__':
    run_bot(CounterBot, {'reply_probability':float})
