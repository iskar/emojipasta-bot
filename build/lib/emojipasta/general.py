from random import choice
from random import randint
import discord
import asyncio
import pyqrcode
import png
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class General():
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def poll(self, ctx, question: str, *options: str):
        optioncount = len(options)
        if optioncount == 1:
            await self.client.say("It's not really a poll if there's only one option.")
            return
        if optioncount > 10:
            await self.client.say("Poll option limit is 10! Try simplifying your question.")
            return
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        msg = ""
        for x, option in enumerate(options):
            msg = msg + "\n{} {}".format(reactions[x], option)

        embed = discord.Embed(title=question, description=msg)
        message = await self.client.say(embed=embed)

        for reaction in reactions[:optioncount]:
            await self.client.add_reaction(message, reaction)

        await self.client.edit_message(message, embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def yn(self, ctx, *args):
        decide_list = [':heavy_check_mark: YES!',':heavy_multiplication_x: NO!']
        decide_answer = choice(decide_list)
        await self.client.say(decide_answer)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def rn(self, ctx, arg1=1, arg2=100):
        try:
            random_number = randint(arg1, arg2)
            await self.client.say("{}-{}: {}".format(arg1, arg2, random_number))
        except ValueError:
            await self.client.say("Invalid range")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def qr(self, ctx, *, msg):
        qr = pyqrcode.create(msg)
        qr.png('qrcode.png', scale=5)
        await self.client.send_file(ctx.message.channel, 'qrcode.png')

def setup(client):
    client.add_cog(General(client))
