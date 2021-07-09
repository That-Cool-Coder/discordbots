import asyncio
from abstract_bot import AbstractBot
from common import run_bot
from pyppeteer import launch

class ImageScraperBot(AbstractBot):
    finding_image = False # Things break when we look for two things at once

    def __init__(self, token: str, debug: bool = False):
        super().__init__(token)
        self.debug = debug

    async def on_ready(self):
        self.TRIGGER = f'hey {self.user.name}'

        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36'
        self.browser = await launch(headless=not self.debug,
            dumpio=self.debug, args=[f'--user-agent={userAgent}', '--no-sandbox'])
        self.page = await self.browser.newPage()
    
    async def on_message(self, message):
        if message.author != self.user:
            if message.content.lower().startswith(self.TRIGGER.lower()):
                if self.finding_image:
                    await message.channel.send('I am already trying to find an image')
                    return

                self.finding_image = True
                # Use try-finally so finding_image is not left incorrect
                try:
                    await message.channel.send('On it!')

                    # Remove trigger from content
                    cleaned_content = message.content[len(self.TRIGGER):]

                    # Goto the google page for the requested image
                    search_terms = cleaned_content.replace(' ', '+')
                    url = f'https://www.google.com/search?q={search_terms}&tbm=isch'
                    await self.page.goto(url)

                    # Wait for the first images to come up
                    await self.page.waitForSelector('.rg_i')
                    thumbnail_elems = await self.page.JJ('.rg_i')

                    # Get an image url
                    # Sometimes the src attribute of a HTML image won't contain
                    # a url but instead some base64-encoded data.
                    # That's bad so we use this loop to ignore base4-encoded ones.
                    image_url = None
                    for elem in thumbnail_elems:
                        await elem.click()
                        await self.page.waitForSelector('.n3VNCb')
                        function_to_run = '() => document.querySelectorAll(".n3VNCb")[0].src'
                        url_candidate = await self.page.evaluate(function_to_run)
                        if not url_candidate.startswith('data:image'):
                            image_url = url_candidate
                            break
                        
                    if image_url is not None:
                        await message.channel.send(image_url)
                    else:
                        await message.channel.send('Error: Could not find an image')
                finally:
                    self.finding_image = False

if __name__ == '__main__':
    run_bot(ImageScraperBot, {'debug':bool})