import random
from common import run_bot
from abstract_bot import Bot

class BruhBot(Bot):
    '''A bot that says a variation of 'bruh' if
    the previous post was a variation of bruh
    '''
    def __init__(self, token: str, reply_probability: float = 1,
        max_bruh_length: int = 20, reversal_probability: float = 0.2):
        super().__init__(token)
        self.reply_probability = reply_probability
        self.max_bruh_length = max_bruh_length
        self.reversal_probability = reversal_probability
    
    async def on_ready(self):
        pass

    async def on_message(self, message):
        # Don't reply to self
        if message.author != self.user:
            # Have a certain chance of replying
            if random.uniform(0, 1) < self.reply_probability:
                if self.is_bruh(message.content) or self.is_bruh(message.content[::-1]):
                    await message.channel.send(self.generate_bruh())
    
    def is_bruh(self, message: str) -> bool:
        '''Return whether message is a variant of the word 'bruh'
        todo: handle possible backward bruhs
        '''

        message = message.lower()

        # remove punctuation, spaces, etc
        message = ''.join(c for c in message if c.isalnum())

        # Check that message contains nothing except chars in bruh
        invalid_chars_present = True in [ch not in 'bruh' for ch in message]
        if invalid_chars_present:
            return False
        
        # Check that the message contains the required characters for a bruh
        # only b and r are required - 'br' is considered to be a valid bruh
        if ('b' not in message) or ('r' not in message):
            return False

        # For each char, check that it should go after the previous one
        is_bruh = True
        for char_idx in range(1, len(message)):
            prev_char = message[char_idx - 1]
            crnt_char = message[char_idx]
            if 'bruh'.index(prev_char) > 'bruh'.index(crnt_char):
                is_bruh = False
                break
        
        return is_bruh
    
    def generate_bruh(self) -> str:
        '''Generate a variation of the word 'bruh'
        '''

        bruh = 'br'
        bruh_length = random.randint(4, self.max_bruh_length)
        h_count = random.randint(1, int(bruh_length / 2))
        u_count = bruh_length - h_count - 2
        bruh += 'u' * u_count + 'h' * h_count
        
        is_reversed = (random.uniform(0, 1) < self.reversal_probability)
        if is_reversed:
            bruh = bruh[::-1] # weird slice results in reversing

        # 50% chance to capitalise first letter
        bruh = random.choice((str.upper, str.lower))(bruh[0]) + bruh[1:]

        return bruh

if __name__ == '__main__':
    run_bot(BruhBot, {'reply_probability':float, 'max_bruh_length':int,
        'reversal_probability': float})
