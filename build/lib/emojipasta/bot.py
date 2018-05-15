from random import choice
from random import randint
import io
import os
import json

from emojigene import EmojipastaGenerator

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import platform
import pyqrcode
import png
import json
import requests
from util.keys import DISCORD_BOT_KEY

client = Bot(description="Emojipasta-Bot is a dicord bot for converting text to emojipasta. \n Bot Owner: toiletplunger#8909 \n Congrats! You don't need to add quotes anymore! ", command_prefix="&", pm_help = False)
client.remove_command("help")

class Bot_Info:

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def count(ctx, *args):
        embed = discord.Embed(description="\n**So here is the server and user count.**")
        embed.add_field(name="💬", value=str(len(client.servers))+ ' **servers**', inline=True)
        embed.add_field(name="🏠", value=str(len(set(client.get_all_members())))+ ' **users**', inline=True)
        await client.say(embed=embed)

    @client.event
    async def on_command_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=str(error))
            embed.set_author(name=ctx.message.author)
            embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
            await client.send_message(ctx.message.channel, embed=embed)
    @client.event
    async def on_command(command, ctx):
        logembed = discord.Embed(description="used the " + str(command) + " command.", timestamp=ctx.message.timestamp)
        logembed.set_author(name=ctx.message.server)
        await client.send_message(discord.Object(id="420586176467042316"), embed=logembed)

    @client.event
    async def on_member_join(member):
        message = "Hello, welcome to Kermit House of Shitposting <@" + member.id + ">! Home of the Emojipasta Bot. We are looking for Python developers. If you are interested, please check <#444895389921837067> :) If not, chill with us and use the bot!!!"
        await client.send_message(discord.Object(id="420586176467042316"), content=message)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def help(ctx, *args):
        await client.say("Check out command list here: https://www.emojipasta.fun/commands/ \nJoin our support server if you need more info: https://discord.gg/JHNRwr6")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def invite(ctx, *args):
        await client.say("https://discordapp.com/oauth2/authorize?client_id=429662497172357123&scope=bot&permissions=8")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def vote(ctx, *args):
        await client.say("https://discordbots.org/bot/429662497172357123")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def orange(ctx, *args):
        await client.say("<@294963984535257089> is my best big titty goth gf <33333")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def github(ctx, *args):
        await client.say("https://github.com/musca1997/emojipasta-bot")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def ping(ctx, *args):
        await client.say(":ping_pong: Pong!")
        await asyncio.sleep(1)
        await client.say(":warning: I'M GAY")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @client.command(pass_context = True)
    async def feedback(ctx, *, user_feedback):
        await client.say("K, already sent your feedback 😎💯 ")
        await client.send_message(discord.Object(id='434726800711483393'), str(ctx.message.author) + ' from <' + str(ctx.message.server) + '> just sent a feedback: ```' + str(user_feedback) + '```')

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def userinfo(ctx, *, user: discord.Member=None):
        """Shows users's informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                                  key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                           if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="Member #{} | User ID:{}"
                                "".format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await client.say(embed=data)
        except discord.HTTPException:
            await client.say("I need the `Embed links` permission "
                                   "to send this")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def serverinfo(ctx):
        """Shows server's informations"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                         if m.status == discord.Status.online or
                         m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len([x for x in server.channels
                                if x.type == discord.ChannelType.voice])
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                         "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                    passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await client.say(embed=data)
        except discord.HTTPException:
            await client.say("I need the `Embed links` permission "
                                  "to send this")

class Bot_Function:

    @commands.cooldown(1, 30, commands.BucketType.user)
    @client.command(pass_context=True)
    async def poll(ctx, question: str, *options: str):
        optioncount = len(options)
        if optioncount == 1:
            await client.say("It's not really a poll if there's only one option.")
            return
        if optioncount > 10:
            await client.say("Poll option limit is 10! Try simplifying your question.")
            return
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        msg = ""
        for x, option in enumerate(options):
            msg = msg + "\n{} {}".format(reactions[x], option)

        embed = discord.Embed(title=question, description=msg)
        message = await client.say(embed=embed)

        for reaction in reactions[:optioncount]:
            await client.add_reaction(message, reaction)

        await client.edit_message(message, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def ud(ctx, *, message: str):
        term = message
        r = requests.get("http://api.urbandictionary.com/v0/define?term=" + term)
        data = json.loads(r.text)
        result = data['result_type']
        if result == "no_results":
            await client.say("No definition was found for *" + term + "*")
            return
        definition = data['list'][0]['definition']
        word = data['list'][0]['word']
        example = data['list'][0]['example']
        tu = str(data['list'][0]['thumbs_up'])
        td = str(data['list'][0]['thumbs_down'])
        embed = discord.Embed(title=word, description=definition + "\n\n*" + example + "*")
        embed.set_footer(text="\U0001F44D " + tu + "  |  \U0001F44E " + td)
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await client.send_message(ctx.message.channel, embed=embed)

    def check_duplicate(users):
        di = dict()
        for u in users:
            if not u in di:
                di.update({u: 0})
            else:
                di.update({u: di.get(u) + 1})
        for key, value in di.items():
            if value > 0:
                return True
    @client.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def brawl(ctx, *users):
        if Bot_Function.check_duplicate(users) == True:
            await client.say("You cannot duplicate brawlers..")
            return
        brawlers = len(users)
        if brawlers > 5:
            await client.say("To prevent this command from filling the chat with spam you are limited to 5 brawlers.")
            return
        elif brawlers == 1:
            await client.say("Are you trying to fight yourself..? More than one brawler is required.")
            return
        combatants = list(users)
        attack = ['punched','kicked','slapped','poked','bit']
        bodypart = ['eyes','mouth','arm','leg','stomach','chest','groin','face']
        users = ", ".join(map(str, users))
        await client.say("Starting a brawl with {}".format(users))
        await asyncio.sleep(3)
        for i in range (len(combatants)):
            if(len(combatants) == 1):
                await client.say("{} is the victor!".format(combatants[0]))
                return
            los = choice(combatants)
            if(len(combatants) == 2):
                vic = choice(combatants)
                if vic == los:
                    combatants.remove(los)
                    vic = combatants[0]
                else:
                    combatants.remove(los)
            elif(brawlers > 2):
                combatants.remove(los)
                vic = choice(combatants)
            atk = choice(attack)
            bpt = choice(bodypart)
            await client.say("{0} has {1} {2} in the {3}! {2} is defeated!".format(vic,atk,los,bpt))
            await asyncio.sleep(5)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def flip(ctx, *, message: str):
        reverse = message[::-1]
        letters = {' ': ' ','z': 'z','y': 'ʎ','x': 'x','w': 'ʍ','v': 'ʌ','u': 'n','t': 'ʇ','s': 's','r': 'ɹ',
        'q': 'b','p': 'd','o': 'o','n': 'u','m': 'ɯ','l': 'l','k': 'ʞ','j': 'ɾ','i': 'ᴉ','h': 'ɥ',
        'g': 'ƃ','f': 'ɟ','e': 'ǝ','d': 'p','c': 'ɔ','b': 'q','a': 'ɐ'}
        newmsg = ""
        for c in reverse:
            if not letters.get(c):
                continue
            newmsg = newmsg + letters[c]
        await client.say(newmsg)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def uw(ctx, message: str = None):
        if message == "list":
            await client.say("Here's the master list of links:\nhttps://pastebin.com/FVhnt8xs")
            return
        f = open(os.path.join("textfiles/randomsites.txt"));
        contents = f.readlines()
        link = ""
        rand = randint(0, len(contents))
        counter = 0
        for i in contents:
            if counter == rand:
                link = i
                break
            else:
                counter+=1
        f.close()
        embed = discord.Embed(description=link + "\nReport a broken link with the &feedback command.")
        embed.set_author(name=ctx.message.author.display_name + " requested a link!", icon_url=ctx.message.author.avatar_url)
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await client.send_message(ctx.message.channel, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def maymay(ctx):
        f = open(os.path.join("textfiles/comics.txt"))
        contents = f.readlines()
        link = ""
        rand = randint(0, len(contents))
        counter = 0
        for i in contents:
            if counter == rand:
                link = i
                break
            else:
                counter+=1
        f.close()
        embed = discord.Embed()
        embed.set_image(url=link)
        await client.say(content="Our :100: devs :ok_hand: enjoy :lion_face::relaxed: them :punch: unironically", embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bw(ctx, message: str = None):
        if message == "list":
            await client.say("Here's the master list of links:\nhttps://pastebin.com/dLe1MdPL")
            return
        f = open(os.path.join("textfiles/bannedsites.txt"))
        contents = f.readlines()
        link = ""
        rand = randint(0, len(contents))
        counter = 0
        for i in contents:
            if counter == rand:
                link = i
                break
            else:
                counter+=1
        f.close()
        embed = discord.Embed(description=link + "\n:flag_cn: Embrace your non-China privilege by visiting a website banned in China! :flag_cn: \nReport a broken link with the &feedback command.")
        embed.set_author(name=ctx.message.author.display_name + " requested a link!", icon_url=ctx.message.author.avatar_url)
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await client.send_message(ctx.message.channel, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def pasta(ctx, *, original_words):
        generator = EmojipastaGenerator.of_default_mappings()
        final_emoji = generator.generate_emojipasta(original_words)

        await client.say(final_emoji)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def yn(ctx, *args):
        decide_list = ['YES!','NO!']
        decide_answer = choice(decide_list)
        await client.say(decide_answer)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def clap(ctx, *, original_clap):
        emojis = [" 👏 "," 👏🏻 "," 👏🏼 "," 👏🏽 "," 👏🏾 "," 👏🏿 "]
        split_clap = original_clap.split()
        new_blocks = []
        for i, block in enumerate(split_clap):
            new_blocks.append(block)
            emoji = choice(emojis)
            new_blocks.append(emoji)
        final_clap = "".join(new_blocks)
        await client.say(final_clap)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def rn(ctx, arg1=1, arg2=100):
        try:
            random_number = randint(arg1, arg2)
            await client.say("{}-{}: {}".format(arg1, arg2, random_number))
        except ValueError:
            await client.say("Invalid range")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def b(ctx, *, message: str):
        newmsg = message.replace("b", "\U0001F171").replace("B", "\U0001f171")
        await client.say(newmsg)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def penislength(ctx, member: discord.Member=None):
        member = member or ctx.message.author
        inches = randint(2, 12)
        cm = inches * 2.54
        text = "8" + ("=" * inches) + "D" + " " + "\U0001F4A6" * (inches // 2)
        reaction = ""
        if inches >= 9:
            reaction = "\U0001F60D Wow! \U0001F60D"
        elif inches <= 4:
            reaction = "Ehh \U0001F612"
        else:
            reaction = "Nice \U0001F609"
        await client.say("{}'s penis is **{} inches!** ({} cm)\n{}\n{}".format(member.mention, inches, cm, text, reaction))

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def spin(ctx, member: discord.Member=None):
        if member:
            member = member
            message = ":regional_indicator_o::regional_indicator_h::warning::regional_indicator_s::regional_indicator_h::regional_indicator_i::regional_indicator_t::exclamation: THIS NI:b::b:A :fire: {} :fire: JUST GOT SPUN ON BY {}! :100: :ok_hand: ".format(member.mention, ctx.message.author.mention)
        else:
            member = ctx.message.author
            message = ":regional_indicator_o::regional_indicator_h::warning::regional_indicator_s::regional_indicator_h::regional_indicator_i::regional_indicator_t::exclamation: THIS NI:b::b:A :fire: {} :fire:JUST SPUN {}! :100: :ok_hand:".format(member.mention, ctx.message.channel.mention)

        embed = discord.Embed()
        embed.set_image(url="https://cdn.discordapp.com/attachments/372188609425702915/436986898641059870/fidget-spinner-gif-transparent-1.gif")
        await client.say(content=message, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def dab(ctx, member: discord.Member=None):
        if member:
            member = member
            message = ":regional_indicator_o::regional_indicator_h::warning::regional_indicator_s::regional_indicator_h::regional_indicator_i::regional_indicator_t::exclamation: THIS NI:b::b:A :fire: {} :fire: JUST GOT DABBED ON BY {}! :100: :ok_hand: ".format(member.mention, ctx.message.author.mention)
        else:
            member = ctx.message.author
            message = ":regional_indicator_o::regional_indicator_h::warning::regional_indicator_s::regional_indicator_h::regional_indicator_i::regional_indicator_t::exclamation: THIS NI:b::b:A :fire: {} :fire:JUST DABBED {}! :100: :ok_hand:".format(member.mention, ctx.message.channel.mention)

        dab_images = [
			"https://cdn.discordapp.com/attachments/428960174808498176/436617301249359903/Dab_1.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617300779728908/DAB.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617300779728906/squidward_dab_by_josael281999-dbbuazm.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617300095795211/Woody_dab.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617300095795210/king_dab__clash_royale__by_josael281999-db8mdhl.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617220714528778/3505ebaa-f270-45d4-8693-88574828ef49.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617219707764736/hitler_hits_a_sick_dab_by_alphashitlord-damch71.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617219091333122/fQh7nCY9K1-8.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617219091333121/dab_2.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617218579759124/a79.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617147230453772/Bearded-Dab.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/439001759168462848/giphy.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439001759168462849/AS003639_09.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439001759860391946/AW386482_01.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439001759860391947/dabpuush_by_discopanda_tm-d9znmse.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439001760447856640/dab_on_em_rose_by_madithekitten-dasw55o.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256214317170688/20162F022F072F862FBettyWhite.f3633.jpg",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256230528155658/d6d.jpg",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256250312556564/giphy.gif",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256264187445260/hqdefault.jpg",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256283821113344/maxresdefault.jpg",
			"https://cdn.discordapp.com/attachments/428960174808498176/439256300107464715/minion_dab_by_julestheocelot-db7yk05.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617146714292236/248.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617146714292235/249480900001211_1.png",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617146173358081/1508659373107.gif",
			"https://cdn.discordapp.com/attachments/420589076916207626/436862948200153088/wubba_lubba_dab_dab_by_alexandratale-dbew3ml.png",
            "https://cdn.discordapp.com/attachments/420589076916207626/439972205003145217/92af322e14246ae1291d06fa9e32223a.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439972589331283978/tenor.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439972589855834115/ee09ebd7068f47c52eff406cf8177c418dbd3e86_hq_by_the8bitdj-dbbdl6e.gif",
            "https://cdn.discordapp.com/attachments/412884243195232257/439972560499769346/dabpuush_by_discopanda_tm-d9znmse.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439973096548597761/ovgeujull8bsku3o_by_theophobic-dbk0904.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439973217038368784/www_gifcreator_me_dj0utn_by_swap_sans-db6yudf.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439973320994324491/harambe.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439973445850365972/062717_milcin_arcia_sedar_dab_med_n9garc16.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439974137927041044/giphy.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439974802183290921/giphy-bdt.gif",
            "https://cdn.discordapp.com/attachments/420589076916207626/439974968537907220/giphy.gif",
            "https://media.discordapp.net/attachments/428960174808498176/443191684981850123/6088d94.png?width=528&height=523",
			"https://cdn.discordapp.com/attachments/428960174808498176/436617144914935829/2e9d4609812ebddeb159f1499e37ec97.png"
		]
        index = randint(0, len(dab_images) - 1)
        embed = discord.Embed()
        embed.set_image(url=dab_images[index])
        await client.say(content=message, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def walk(ctx, member: discord.Member=None):
        if member:
            member = member
            message = "( ͡° ͜ʖ ͡°) ╯╲___卐卐卐卐卐 Don't mind me just taking {} for a walk!".format(member.mention)
        else:
            member = ctx.message.author
            message = "( ͡° ͜ʖ ͡°) ╯╲___ Who wants to go for a walk??"

        await client.say(message)

    @client.command(pass_context=True)
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def jerkit(ctx):
        msg = await client.say("8:fist:====D")
        await asyncio.sleep(.2)
        await client.edit_message(msg,"8=:fist:===D")
        await asyncio.sleep(.3)
        await client.edit_message(msg,"8==:fist:==D")
        await asyncio.sleep(.4)
        await client.edit_message(msg,"8===:fist:=D")
        await asyncio.sleep(.5)
        await client.edit_message(msg,"8====:fist:D")
        await asyncio.sleep(.6)
        await client.edit_message(msg,"8===:fist:=D")
        await asyncio.sleep(.5)
        await client.edit_message(msg,"8==:fist:==D")
        await asyncio.sleep(.4)
        await client.edit_message(msg,"8=:fist:===D")
        await asyncio.sleep(.3)
        await client.edit_message(msg,"8:fist:====D")
        await asyncio.sleep(.2)
        await client.edit_message(msg,"8:fist:====D:sweat_drops:")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def qr(ctx, *, msg):
        qr = pyqrcode.create(msg)
        qr.png('qrcode.png', scale=5)
        await client.send_file(ctx.message.channel, 'qrcode.png')

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def owo(ctx, *, message: str):
        newmsg = message.replace("r", "w").replace("l", "w")
        await client.say("**O**w**O** " + newmsg + " **O**w**O**")

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def mock(ctx, *, message: str = None):
        channel = ctx.message.channel
        if not message:
            msg = "my name is " + ctx.message.author.mention + " and I don't know how to properly use the mock command"
        else:
            msg = message.lower()
        newmsg = ""
        for c in msg:
            rand = randint(0, 1)
            if rand:
                newmsg = newmsg + c.upper()
            else:
                newmsg = newmsg + c

        embed = discord.Embed(description=newmsg)
        embed.set_thumbnail(url="http://i.imgur.com/upItEiG.jpg")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await client.send_message(channel, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def shrek(ctx):
        channel = ctx.message.channel
        author = ctx.message.author
        message = author.mention + " has invited Shrek to visit " + channel.mention + "!"
        embed = discord.Embed(description=message)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/421005964276138005/434538229438349313/Shrek_emoji.png")
        embed.colour = ctx.message.author.colour if hasattr(ctx.message.author, "colour") else discord.Colour.default()
        await client.send_message(channel, embed=embed)

    @client.command(pass_context=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def d(ctx):
        d = ["DES", "PA", "CITO"]
        for i in d:
            await client.say(i)
            await asyncio.sleep(1)

    @client.command(pass_context=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def t(ctx):
        f = open(os.path.join("textfiles/memetemplates.txt"))
        contents = f.readlines()
        link = ""
        rand = randint(0, len(contents))
        counter = 0
        for i in contents:
            if counter == rand:
                link = i
                break
            else:
                counter+=1
        f.close()
        embed = discord.Embed()
        embed.set_image(url=link)
        await client.say(content="OK here's the random blank meme template for you!", embed=embed)

    @client.event
    async def on_server_join(server):
        server = server
        online = len([m.status for m in server.members
                         if m.status == discord.Status.online or
                         m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len([x for x in server.channels
                                if x.type == discord.ChannelType.voice])

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description="",
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await client.send_message(discord.Object(id="436544688745480203"), content="I just got **added** into a new server! Now I'm in " + str(len(client.servers)) + " servers with " + str(len(set(client.get_all_members()))) + " users.", embed=data)
        except discord.HTTPException:
            await client.say("I need the `Embed links` permission "
                                  "to send this")

    @client.event
    async def on_server_remove(server):
        server = server
        online = len([m.status for m in server.members
                         if m.status == discord.Status.online or
                         m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len([x for x in server.channels
                                if x.type == discord.ChannelType.voice])

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description="",
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await client.send_message(discord.Object(id="436544688745480203"), content="I just got **removed** from this server. Press XD to pay respect. Now I'm in " + str(len(client.servers)) + " servers with " + str(len(set(client.get_all_members()))) + " users.", embed=data)
        except discord.HTTPException:
            await client.say("I need the `Embed links` permission "
                                  "to send this")

class Restricted:
    @client.command(pass_context=True)
    async def status(ctx,  *, new_stat):
        new_stat = "&help | " + new_stat
        if (str(ctx.message.author.id) == "349838216637186048" or str(ctx.message.author.id)  == "396783619466854402" or str(ctx.message.author.id)  == "183457916114698241" or str(ctx.message.author.id)  == "294963984535257089"):
            await client.change_presence(game=discord.Game(name=(new_stat)))
            await client.say("Done.")
        else:
            await client.say("HAHA CUCKED U DONT HAVE THE PERMISSION TO CHANGE MY STATUS.")

    @client.event
    async def on_message(message):
        await client.process_commands(message)
        if not (message.channel.id == "431202784575094794" or message.channel.id == "442488016523624448"):
            return
        if not message.attachments:
            return
        files = {"431202784575094794": "memetemplates.txt", "442488016523624448": "comics.txt"}
        url = str(message.attachments[0]['url'])
        extensions = ["png", "gif", "jpg", "jpeg"]
        length = len(url)
        index = 1
        for x in range(2, length):
            if url[-x] == ".":
                break
            else:
                index+=1
        ext = url[-index:].lower()
        if ext not in extensions:
            return
        f = open(files[str(message.channel.id)], 'a')
        f.write(url + '\n')
        f.close()
        embed = discord.Embed(description="File added to " + files[str(message.channel.id)] + " by " + str(message.author))
        await client.send_message(discord.Object(id="436544688745480203"), embed=embed)

def main():
    @client.event
    async def on_ready():
    	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    	print('--------')
    	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    	print('--------')
    	print('Use this link to invite {}:'.format(client.user.name))
    	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    	print('--------')
    	print('--------')

    cogs = ['image', 'moderation', 'frames', 'emojibomb']
    for cog in cogs:
        client.load_extension(cog)

    client.run(DISCORD_BOT_KEY)

if __name__ == "__main__":
    main()
