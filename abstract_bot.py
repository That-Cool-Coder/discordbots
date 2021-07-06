import discord
import asyncio

class AbstractBot:
    client = discord.Client()
    user = None

    def __init__(self, token):
        self.token = token

        @self.client.event
        async def on_ready():
            self.__on_ready()
        
        @self.client.event
        async def on_message(message):
            self.__on_message(message)
        
    def run(self):
        self.client.run(self.token)
    
    def __on_ready(self):
        print(f'Logged in as {self.client.user}')
        self.user = self.client.user
        self.on_ready()
    
    def on_ready(self):
        '''Placeholder function to be overwitten'''
        pass

    def  __on_message(self, message):
        self.on_message(message)
    
    def on_message(self, message):
        '''Placeholder function to be overwritten'''
        pass

    def reply_to_message(self, message, reply):
        async def a():
            await message.channel.send(reply)
        asyncio.ensure_future(a())