#!/usr/bin/env python3
import discord
import asyncio
from discord.ext import commands

TOKEN = 'NjA2MDc2MDk5NDQ0NjA0OTU4.XUFynQ.TaJfvqkSNrOhb06j14CDd73ntpc'

go_paper = -1
memb = set()
chan_inv = 'https://discord.gg/B7sCXkC'
res_sleeper = 606440047469789202
v_ch_id = 606417138177277982
txt_ch_id = 606435892541915137


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.my_task())

    async def on_ready(self):
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('-----------')

    async def my_task(self):
        global go_paper
        while go_paper != 1:
            await asyncio.sleep(1)
        await self.wait_until_ready()
        go_paper = 2
        vc_channel = self.get_channel(v_ch_id)
        txt_channel = self.get_channel(txt_ch_id)
        not_go = True
        while not_go:
            inv_set = set()
            for vis_id in memb:
                if self.get_user(vis_id) not in vc_channel.members:
                    inv_set.add(vis_id)
            if len(inv_set) == 0:
                not_go = False
            else:
                msg = ''
                for vis_id in inv_set:
                    msg += self.get_user(vis_id).mention + ', '
                msg += 'please enter the channel ' + chan_inv
                await txt_channel.send(msg)
            await asyncio.sleep(7)
        await txt_channel.send('That\'s it, we are ready to start!')
        await txt_channel.send('Now you will be turned the sound off one by one')
        await txt_channel.send('Other players will have about 1 minute for decision')

        for mem in vc_channel.members:
            await mem.edit(mute=True, deafen=True)
            msg = mem.mention + " don't hear you! Imagine something cool!"
            await txt_channel.send(msg)
            await txt_channel.send('If you are ready just write !ready in this chat')
            await self.wait_for('message', check=lambda m: m.content == '!ready')
            await mem.edit(mute=False, deafen=False)
            await txt_channel.send('Alright! Moving on!')


bot = Bot('!')


@bot.event
async def on_message(message):
    global go_paper

    if message.author == bot.user:
        return

    if message.content.startswith('!end'):
        msg = 'Ending event.'.format(message)
        go_paper = -1
        memb.clear()
        await message.channel.send(msg)

    if message.content.startswith('!start'):
        msg = 'Starting event.'.format(message)
        go_paper = 1
        await message.channel.send(msg)

    if go_paper == 0:
        if message.author.id not in memb:
            memb.add(message.author.id)
            msg = 'Welcome to the game, buddy {0.author.mention}'.format(message)
            await message.channel.send(msg)
        else:
            msg = 'Oh shit, i am sorry, you are already in game, {0.author.mention}'.format(message)
            await message.channel.send(msg)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!help'):
        msg = 'Hello! I am useless bot.'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!paper'):
        msg = 'Wow! Let\'s play event \"Bumazshki\"! If you want to be invited, write something ih this chat.'.format(
            message)
        go_paper = 0
        await message.channel.send(msg)


bot.run(TOKEN)
