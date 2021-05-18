import discord
import random
import discord, json, pyfiglet
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.ext.commands import *
from discord.ext.commands import BucketType
import asyncio
from asyncio import sleep

bot = commands.Bot(description="yo", command_prefix="!", self_bot=True)
channel_names = ['Channel', 'Names']
bot.remove_command('help')

@bot.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member):
    await ctx.message.delete()
    embed = discord.Embed(title=f"Profil de: {member.name}", color=0xffee00)
    embed.add_field(name="Créé le:", value=f"{member.created_at.strftime('%d.%m.%Y, %H:%M Heure')}")
    embed.add_field(name="Rejoind le:", value=f"{member.joined_at.strftime('%d.%m.%Y, %H:%M Heure')}")
    embed.add_field(name="Pseudo:", value=f"{member.nick}")
    embed.add_field(name="Activité", value=f"{member.activity}")
    embed.add_field(name="Rôles:", value=f"{member.top_role}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_footer(text=f"Demandé par: {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def ascii(ctx, *, args):
    await ctx.message.delete()
    text = pyfiglet.figlet_format(args)
    await ctx.send(f'```{text}```')
    

snipe_message_content = None
snipe_message_author = None

@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author

    snipe_message_content = message.content
    snipe_message_author = message.author.name 
    await asyncio.sleep(60)
    snipe_message_author = None 
    snipe_message_content = None

@bot.command()
async def snipe(message):  
    if snipe_message_content==None:
        await message.channel.send("Il n'y a rien a snipe ici !")
    else:
        embed = discord.Embed(description=f"{snipe_message_content}", color=0xab0000,)
        embed.set_footer(text=f"Demandé par {message.author.name}#{message.author.discriminator}")
        embed.set_author(name = f"Snipe le message supprimer par : {snipe_message_author}")
        await message.channel.send(embed=embed)
        return

@bot.command(pass_context=True)
async def ccr(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()
    for i in range(1):
            await guild.create_text_channel(random.choice(channel_names))
    while True:
        for channel in guild.text_channels:
                for i in range(500):
                    await guild.create_text_channel(random.choice(channel_names))

@bot.command(pass_context=True)
async def cdel(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()

    for channel in list(ctx.message.guild.channels):
        try:
            await channel.delete()
            print(f"{channel.name} a été supprimé")
        except:
            pass

@bot.command()
async def embed(ctx, *, description):
    await ctx.message.delete()
    embed=discord.Embed(description=description, color=0x7f03fc,)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    await ctx.message.delete()
    member = ctx.author if not member else member
    embed = discord.Embed(title = f"{member.name} avatar", color = member.color, timestamp= ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Demandé par: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await asyncio.sleep(1)
    print(f'{bot.user} est connecté !')

with open('./config.json') as f:
    config = json.load(f)

token = config.get('token')
bot.run(token, bot=False)