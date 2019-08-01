import discord
import asyncio

TOKEN = 'NjA2MDc2MDk5NDQ0NjA0OTU4.XUFynQ.TaJfvqkSNrOhb06j14CDd73ntpc'

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        print('a')
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(606415393371979792) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60) # task runs every 60 seconds


client = MyClient()
client.run(TOKEN)