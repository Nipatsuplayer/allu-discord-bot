import os
import logging
import discord
import json
import asyncio
import platform
import psutil
import datetime
import praw
import requests
from discord import app_commands, Interaction
from discord.ext import commands, tasks
import io
import random
import topgg

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.presences = True

start_time = datetime.datetime.now()

reddit = praw.Reddit(
    client_id=os.getenv("redditid"),
    client_secret=os.getenv("redditsecret"),
    user_agent='nexus discord bot by nipatsu & blaze'
)

restart = discord.Embed(title="<a:success:1199386056794046575> ALLU IS RESTARTED",
                      description="```\nAllu is now restarted. You can use commands normally!\n```",
                      colour=0x0ce910)

client = commands.Bot(command_prefix='?', intents=intents)
client.remove_command('help')

ads_list = ["🌟 Welcome to Sprites Developments Network!🌟\nAre you ready to level up your skills in web development, Discord bot creation, or Fivem development? Look no further! Join our vibrant community today and dive into the world of coding excellence.\n🚀 What We Offer:\n* Expert guidance in web development, Discord bot creation, and Fivem development.\n* Collaborative environment to share ideas and learn from like-minded individuals.\n* Access to cutting-edge resources and tools to enhance your development journey.\n💻 Connect with Us:\n🔗 Website: https://www.discordbotking.co.uk\n🔗 Discord Server: https://discord.gg/pPm29ECmNV\nDon't miss out on this opportunity to be part of something extraordinary. Join Sprites Developments Network and unlock your full potential today! See you there!", "**Codewave - The coding server**\nEver wanted to talk with other developers or ever wanted a bot? **Codewave** is for you!\n\nSome of our features are:\n🫂 Active community - Our community is small but active and, some may even offer a helping hand! 🫂 \n🛡️  Security - We use VPN for our services, assuring no one will know your data you shared with us! 🛡️ \n💰 Cheap - All our services are within an affordable and reasonable price. 💰 \n⏩ Fast - All our customers will get their product as fast as possible! ⏩ \n🎉 Giveaways - We are doing frequent giveaways for some of our products! 🎉 \n😱 AND MORE 😱 \n=> JOIN OUR COMMUNITY NOW BY CLICKING BELOW <=\nhttps://discord.gg/cyqm4Ej3fC"]

async def setup_topgg():
    dbl_token = os.getenv("topgg_token")
    return topgg.DBLClient(client, dbl_token)

premium = {"servers": []}


tree = client.tree

@client.event
async def on_ready():
    print("----------ALLU----------")
    logging.info(f'Logged in as {client.user.name} (ID: {client.user.id})')
    await client.tree.sync()
    print("-----Slash commands synced-----")
    client.dblpy = await setup_topgg()
    channel = client.get_channel(1136297435505897530)
    await channel.send(embed=restart)
    print("-----Restart message sent-----")
    update_status.start()

@discord.ext.tasks.loop(minutes=10)
async def update_status():
    guild_count = len(client.guilds)
    status = f"/help | {guild_count} servers"

    await client.change_presence(activity=discord.Game(name=status))
    
@client.event
async def on_guild_join(guild):
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            if channel.permissions_for(guild.me).send_messages:
                newserveremb = discord.Embed(title="__Thanks for inviting me!__",
                      description="Congrats! You just added new cool feature to your discord server.<:allu:1199387263721803927>\n\n**Some links:**\n[Website](https://allu2.godaddysites.com/main) | [Top.gg](https://top.gg/bot/1134746550325739590) | [Youtube](https://www.youtube.com/@CodeWithAllu) | [Support Server](https://discord.gg/xk6SmkjFhr)\n\n<a:info:1174982068481036369>**Use command </help:1136308327777849364> to get help**\n\n**Have Fun!** <a:fun:1174982531112775680>",
                      colour=0x2900f5)
                newserveremb.set_thumbnail(url="https://cdn.discordapp.com/avatars/1134746550325739590/a_50ad9f551bf254869a1d834294737548.gif?size=1024")
                await channel.send(embed=newserveremb)
                break
    
@tree.error
async def on_app_command_error(
    interaction: Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingPermissions):
        error_message = str(error)
        if ":" in error_message:
            missing_perms = error_message.split(":")[1].strip()
        else:
            missing_perms = error_message
        noperms = discord.Embed(title="<a:wrong:1199385940263706765> ERROR",
                      description=f"```\nNO PERMISSIONS TO USE THIS COMMAND\n```\n**REQUIRED PERMISSIONS:**\n```\n{missing_perms}\n```",
                      colour=0xf50000)
        await interaction.response.send_message(embed=noperms, ephemeral=True)
    elif isinstance(error, (app_commands.MissingPermissions, app_commands.BotMissingPermissions)):
        error_message = str(error)
        if ":" in error_message:
            missing_perms = error_message.split(":")[1].strip()
        else:
            missing_perms = error_message
        noperms = discord.Embed(title="<a:wrong:1199385940263706765> ERROR",
                      description=f"```\nBOT DON'T HAVE PERMISSIONS TO DO THIS\n```\n**REQUIRED PERMISSIONS:**\n```\n{missing_perms}\n```",
                      colour=0xf50000)
        await interaction.response.send_message(embed=noperms, ephemeral=True)
    elif isinstance(error, app_commands.CommandOnCooldown):
        cooldown = discord.Embed(title="<a:wrong:1199385940263706765> ERROR",
                      description=f"```\nYOU NEED TO WAIT {error.retry_after:.2f} BEFORE TRYING THIS COMMAND AGAIN.\n```",
                      colour=0xf50000)
        await interaction.response.send_message(embed=cooldown, ephemeral=True)
    elif isinstance(error, app_commands.MissingRole):
        if ctx.command.name in [""]:
            await ctx.send("You need premium to use this command")
    else:
        error = discord.Embed(title="<a:wrong:1199385940263706765> ERROR",
                      description=f"**SOMETHING WEIRD HAPPENED!?**\n__**SEND THIS ERROR CODE TO BOT DEVELOPERS:**__\n\n```\n{error}\n```",
                      colour=0xf50000)
        await interaction.response.send_message(embed=error, ephemeral=True)
        
        
@client.tree.command(name = "help", description = "Info about commands and bot")
async def help(interaction):
    user_id = interaction.user.id
    votething = False
    has_voted = await client.dblpy.get_user_vote(user_id)
    if not has_voted:
        if random.randint(1, 10) == 1:
            ad = random.choice(ads_list)
            adembed = discord.Embed(title="IT'S AD TIME!!!",
                      description=f"{ad}",
                      colour=0x00b0f4)
            adembed.set_footer(text="ADs will last for 10 seconds")
            await interaction.response.send_message(embed=adembed, ephemeral=True)
            await asyncio.sleep(10)
            votething = True
    helpcmd = discord.Embed(title="<:allu:1199387263721803927> HELP",
                      description="Allu is all in one discord bot made by Nipatsu and BlazingViking.\n\n[Website](https://allu2.godaddysites.com/main) | [Youtube](https://www.youtube.com/@CodeWithNexus) | [Discord](https://discord.gg/U4AXhf7Et9)\n\n**COMMANDS:** \n Commands are here now: https://allu2.godaddysites.com/commands",
                      colour=0x2b2d31)

    helpcmd.set_image(url="https://share.creavite.co/65afefcd7b584672641d1ac4.gif")
    if votething is False:
        await interaction.response.send_message(embed=helpcmd, ephemeral=True)
    else:
        await interaction.followup.send(embed=helpcmd, ephemeral=True)

@client.tree.command(name = "meme", description = "Get random meme from reddit")
async def meme(interaction):
        subreddit = reddit.subreddit('memes')
        random_post = subreddit.random()

        memecmd = discord.Embed(
            title=random_post.title,
            url=f'https://www.reddit.com{random_post.permalink}',
            color=0x2b2d31
        )
        memecmd.set_image(url=random_post.url)
        memecmd.set_author(name="REDDIT MEMES",
                 icon_url="https://www.redditinc.com/assets/images/site/Reddit_Icon_FullColor-1_2023-11-29-161416_munx.jpg")
        memecmd.set_footer(text=f'👍 {random_post.score} 👎 {random_post.num_comments}')
        await interaction.response.send_message(embed=memecmd, ephemeral=True)

@client.tree.command(name = "dadjoke", description = "Get random dadjoke")
async def dadjoke(interaction):
            response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
            response.raise_for_status()  
            data = response.json()
            joke = data.get('joke')
            dadjoke = discord.Embed(title="<a:joke:1199750762947940444> DADJOKE",
                      description=f"```\n{joke}\n```",
                      colour=0x2b2d31)
            await interaction.response.send_message(embed=dadjoke)
            
@client.tree.command(name = "avatar", description = "Get your or other user avatar")
@app_commands.describe(
  user="User whos avatar you want to see"
)
async def avatar(
  interaction: discord.Interaction,
  user: discord.Member = None
):
        if user is None:
            user = interaction.user
        else:
            user = user

        avatar_url = user.avatar.url
        avatarcmd = discord.Embed(title=f"{user.name}'s Avatar", color=0x2b2d31)
        avatarcmd.set_image(url=avatar_url)

        avatar_url_original = user.avatar.url
        avatarcmd.add_field(name="Download Link", value=f"[Original]({avatar_url_original})", inline=False)
        await interaction.response.send_message(embed=avatarcmd)
        
@client.tree.command(name = "ban", description = "Ban users")
@app_commands.guild_only()
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.checks.bot_has_permissions(ban_members=True)
@app_commands.describe(
  user="User who you want to ban",
  reason="Why you ban user"
)
async def ban(
  interaction: discord.Interaction,
  user: discord.Member,
  reason: str = None):
        if user == interaction.user:
            await interaction.response.send_message("Hey, you can't ban yourself!", ephemeral=True)
        elif user.bot:
            await interaction.response.send_message("Hey, you can't ban bots!", ephemeral=True)
        else:
            if reason is None:
                reason = "None"
            else:
                reason = reason
            user2 = interaction.user
            ban1 = discord.Embed(title="<a:moderation:1174982191172833381> BANNED!!",
                      description=f"{user}, You have been banned from `{interaction.guild.name}`!",
                      colour=0xf50018)

            ban1.set_author(name=f"Moderator: {user2.name}",
                 icon_url=f"{user2.avatar.url}")

            ban1.add_field(name="REASON:",
                value=f"```\n{reason}\n```",
                inline=False)
            if interaction.guild.me.guild_permissions.ban_members:
                try:
                    await user.send(embed=ban1)
                except discord.Forbidden:
                    pass
            await interaction.guild.ban(user, reason=reason)
            ban2 = discord.Embed(title="<a:moderation:1174982191172833381> BANNED!",
                      description=f"**<a:success:1199386056794046575> Succesfully banned {user}!**",
                      colour=0xf50018)

            ban2.add_field(name="REASON:",
                value=f"```\n{reason}\n```",
                inline=False)
            await interaction.response.send_message(embed=ban2, ephemeral=True)
                                                
@client.tree.command(name = "kick", description = "Kick users")
@app_commands.guild_only()
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.checks.bot_has_permissions(kick_members=True)
@app_commands.describe(
  user="User who you want to kick",
  reason="Why you kick user"
)
async def kick(
  interaction: discord.Interaction,
  user: discord.Member,
  reason: str = None):
    if user == interaction.user:
            await interaction.response.send_message("Hey, you can't kick yourself!", ephemeral=True)
    elif user.bot:
            await interaction.response.send_message("Hey, you can't kick bots!", ephemeral=True)
    else:
        if reason is None:
            reason = "None"
        else:
            reason = reason
        user2 = interaction.user
        kick1 = discord.Embed(title="<a:moderation:1174982191172833381> KICKED!!",
                      description=f"{user}, You have been kicked from `{interaction.guild.name}`!",
                      colour=0xf50018)

        kick1.set_author(name=f"Moderator: {user2.name}",
                 icon_url=f"{user2.avatar.url}")

        kick1.add_field(name="REASON:",
                value=f"```\n{reason}\n```",
                inline=False)
        if interaction.guild.me.guild_permissions.kick_members:
                try:
                    await user.send(embed=kick1)
                except discord.Forbidden:
                    pass
        await interaction.guild.kick(user, reason=reason)
        kick2 = discord.Embed(title="<a:moderation:1174982191172833381> KICKED!",
                      description=f"**<a:success:1199386056794046575> Succesfully kicked {user}!**",
                      colour=0xf50018)

        kick2.add_field(name="REASON:",
                value=f"```\n{reason}\n```",
                inline=False)
        await interaction.response.send_message(embed=kick2, ephemeral=True)
            
@client.tree.command(name="about",description="Interesting stats about bot")
async def ping(interaction: discord.Interaction):
    latency = client.latency
    python_version = platform.python_version()
    disk_usage = psutil.disk_usage('/')
    total_disk_gb = disk_usage.total / (1024 ** 3)
    used_disk_gb = disk_usage.used / (1024 ** 3)
    ram = psutil.virtual_memory()
    total_ram_gb = ram.total / (1024 ** 3)
    used_ram_gb = ram.used / (1024 ** 3)
    uptime_delta = datetime.datetime.now() - start_time
    uptime_days = uptime_delta.days
    uptime_hours, remainder = divmod(uptime_delta.seconds, 3600)
    uptime_minutes, uptime_seconds = divmod(remainder, 60)
    uptime_str = f'{uptime_days} Days {uptime_hours} hours, {uptime_minutes} minutes, {uptime_seconds} seconds'
    total_user_count = sum(guild.member_count for guild in client.guilds)
    server_count = len(client.guilds)
    aboutemb = discord.Embed(title="Allu Discord Bot",
                      colour=0xf1f500)

    aboutemb.add_field(name="GENERAL INFO",
                value=f"<a:arrow:1210967259992948756> **Developers:** `nipatsuyt, blaze_official`\n<a:arrow:1210967259992948756> **Python version: ** `{python_version}`\n<a:arrow:1210967259992948756> **Uptime:** `{uptime_str}`",
                inline=False)
    aboutemb.add_field(name="STATS",
                value=f"<a:arrow:1210967259992948756> **Ping:** `{round(latency * 1000)}ms`\n<a:arrow:1210967259992948756> **RAM usage:** `{used_ram_gb:.2f}GB / {total_ram_gb:.2f}GB`\n<a:arrow:1210967259992948756> **Disk Space:** `{used_disk_gb:.2f}GB / {total_disk_gb:.2f}GB`\n<a:arrow:1210967259992948756> **Servers:** `{server_count}`\n<a:arrow:1210967259992948756> **Users:** `{total_user_count}`", inline=False)
    await interaction.response.send_message(embed=aboutemb)
            
@client.tree.command(name="unban", description="unban user")
@app_commands.guild_only()
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(
  user="Put user ID here"
)
async def unban(interaction: discord.Interaction, user: int):
    unban = discord.Embed(title="<a:moderation:1174982191172833381> UNBANNED!",
                      description=f"**<a:success:1199386056794046575> Succesfully unbanned {user}!**",
                      colour=0xf50018)
    try:
        guild = interaction.guild
        await guild.unban(user)
        await interaction.response.send_message(embed=unban, ephemeral=True)
    except discord.NotFound:
        await interaction.response.send_message("User not found", ephemeral=True)
    
@client.tree.command(name="partners", description="Our amazing partners!")
async def partners(interaction: discord.Interaction):
    partners = discord.Embed(title="PARTNERS",
                      colour=0x00b0f4)

    partners.add_field(name="Codewave - The coding server",
                value="Ever wanted to talk with other developers or ever wanted a bot? **Codewave** is for you!\n\nSome of our features are:\n🫂 Active community - Our community is small but active and, some may even offer a helping hand! 🫂 \n🛡️  Security - We use VPN for our services, assuring no one will know your data you shared with us! 🛡️ \n💰 Cheap - All our services are within an affordable and reasonable price. 💰 \n⏩ Fast - All our customers will get their product as fast as possible! ⏩ \n🎉 Giveaways - We are doing frequent giveaways for some of our products! 🎉 \n😱 AND MORE 😱 \n=> JOIN OUR COMMUNITY NOW BY CLICKING BELOW <=\nhttps://discord.gg/cyqm4Ej3fC\n\n--------------------------------------------------",
                inline=False)
    partners.add_field(name="🌟 Welcome to Sprites Developments Network! 🌟",
                value="Are you ready to level up your skills in web development, Discord bot creation, or Fivem development? Look no further! Join our vibrant community today and dive into the world of coding excellence.\n🚀 What We Offer:\n* Expert guidance in web development, Discord bot creation, and Fivem development.\n* Collaborative environment to share ideas and learn from like-minded individuals.\n* Access to cutting-edge resources and tools to enhance your development journey.\n💻 Connect with Us:\n🔗 Website: https://www.discordbotking.co.uk\n🔗 Discord Server: https://discord.gg/pPm29ECmNV\nDon't miss out on this opportunity to be part of something extraordinary. Join Sprites Developments Network and unlock your full potential today! See you there!",
                inline=False)
    await interaction.response.send_message(embed=partners)
    
@client.tree.command(name = "userinfo", description = "All possible info about you or someone else")
@app_commands.describe(
  user="User whos info you want to view")
async def userinfo(
  interaction: discord.Interaction,
  user: discord.Member = None):
    if user is None:
        user2 = interaction.user
    else:
        user2 = user
    joineddiscord = user2.created_at.timestamp()
    joinedserver = user2.joined_at.timestamp()
    roles = ', '.join([role.name for role in user2.roles])
    if user2.premium_since is None:
        isbooster = 'User is not a booster'
    else:
        isbooster = 'User is a booster'
    user_badges_flags = {
            "hypesquad_bravery": "<:braverybadge:1237791318604906577>",
            "hypesquad_balance": "<:balancebadge:1237791246278459394>",
            "hypesquad_brilliance": "<:brilliancebadge:1237790451248140409>",
            "hypesquad": "<:hypesquadeventsbadge:1237791113738190869>",
            "partner": "<:partnerbadge:1237790610837209218>",
            "verified_bot_developer": "<:earlydeveloperbadge:1237791816036778097>",
            "active_developer": "<:activedeveloperbadge:1237790946129739828>",
            "bug_hunter_lvl_1": "<:bughunterbadge:1237790732279091280>",
            "early_supporter": "<:earlysupporterbadge:1237787024606498877>",
            "staff": "<:staffbadge:1237790548937408592>",
            "discord_certified_moderator": "<:discordmodbadge:1237791913919123467>",
        }
    misc_flags_descriptions = {
            "team_user": "Application Team User",
            "system": "System User",
            "spammer": "Spammer",
            "verified_bot": "Verified Bot",
            "bot_http_interactions": "HTTP Interactions Bot",
        }

    set_flags = {flag for flag, value in user2.public_flags if value}
    subset_flags = set_flags & user_badges_flags.keys()
    badges = [user_badges_flags[flag] for flag in subset_flags]
    member = interaction.guild.get_member(user2.id)
    if str(member.status) == "online":
        status = '<:online:1138327529766264872>'
    elif str(member.status) == "offline":
        status = '<:offline:1138327585516961833>'
    elif str(member.status) == "idle":
        status = '<:idle11:1239983290744574035>'
    elif str(member.status) == "dnd":
        status = '<:dnd11:1239983372328112148>'
    else:
        status = 'Unknown Status :question:'

    embed = discord.Embed(title="USER INFO",
                      colour=0x00b0f4)

    embed.set_author(name=f"{user2.name}",
                 icon_url=f"{user2.avatar.url}")

    embed.add_field(name="<:image_id:1238505158367776829> USER ID",
                value=f"```\n{user2.id}\n```",
                inline=True)
    embed.add_field(name="<:create:1238505341688221807> ACCOUNT CREATED",
                value=f"<t:{int(joineddiscord)}:F>",
                inline=True)
    embed.add_field(name="<:ServerJoin:1238505499566149673> JOINED SERVER",
                value=f"<t:{int(joinedserver)}:F>",
                inline=True)
    embed.add_field(name="<:Roles:1238505606227296306> ROLES",
                value=f"{roles}",
                inline=True)
    embed.add_field(name="<:boost:1138328347282251777> BOOSTER?",
                value=f"```\n{isbooster}\n```",
                inline=True)
    embed.add_field(name="<a:badges:1238505728042340422> BADGES",
                value=" ".join(badges),
                inline=True)
    embed.add_field(name="<a:IconUserStatus:1238505958049841262> STATUS",
                value=f"{status}",
                inline=True)
    await interaction.response.send_message(embed=embed)
    
@client.tree.command(name="updates", description="Check latest updates")
async def updates(interaction: discord.Interaction):
    updtchannel_id = 1136297435505897531
    updtchannel = client.get_channel(updtchannel_id)
    if updtchannel is None:
        await interaction.response.send_message("Channel not found.")
        return

    messages = [message async for message in updtchannel.history(limit=1)]
    if messages:
        latest_message = messages[0]
        message_link = latest_message.jump_url
        timestamp = int(latest_message.created_at.timestamp())
        embed = discord.Embed(
            title="__LATEST UPDATE__",
            url=f"{message_link}",
            description=f"**Update published:** <t:{timestamp}:f>",
            colour=0x00b0f4
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.followup.send(f"{latest_message.content}", ephemeral=True)

        
    
client.run(os.environ["token"])