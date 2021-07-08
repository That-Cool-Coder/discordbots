import discord
import asyncio

class Bot:
    client = discord.Client()

    def __init__(self, token):
        self.token = token

        print('Bot initiated')

        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user}')
        
        @self.client.event
        async def on_message(message):
            print(message.content)
        
    async def run(self):
        print('Bot running')
        self.client.run(self.token)

if __name__ == '__main__':
    bot1 = Bot('')
    bot2 = Bot('')
    loop = asyncio.get_event_loop()
    loop.create_task(bot1.run())
    loop.create_task(bot2.run())
    loop.run_forever()