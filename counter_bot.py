from common import run_bot
from abstract_bot import AbstractBot

class CounterBot(AbstractBot):
    '''A bot that says counts up.
    If the previous post is an integer, add one and post that'''

    def on_message(self, message):
        # Don't reply to selt
        if message.author != self.user:
            # Only proceed if message is integer (ie only digits)
            if message.content.isdigit():
                self.reply_to_message(message, int(message.content) + 1)

if __name__ == '__main__':
    run_bot(CounterBot)