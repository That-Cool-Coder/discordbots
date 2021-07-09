import discord
import asyncio

class AbstractBot:
    client = discord.Client()
    user = None

    def __init__(self, token):
        self.token = token

        @self.client.event
        async def on_ready():
            await self.__on_ready()
        
        @self.client.event
        async def on_message(message):
            await self.__on_message(message)
        
    def run(self):
        self.client.run(self.token)
    
    async def __on_ready(self):
        print(f'Logged in as {self.client.user}')
        self.user = self.client.user
        await self.on_ready()
    
    async def on_ready(self):
        '''Placeholder function to be overwitten'''
        pass

    async def  __on_message(self, message):
        await self.on_message(message)
    
    async def on_message(self, message):
        '''Placeholder function to be overwritten'''
        pass