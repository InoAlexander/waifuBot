# darling discord Bot, this is a work in progress... i have a ton of features i want to add but i have badly unmanaged ADHD to i kind of just work on this when i can or feel the spark... its super weeboid sooo deal with it.

import os
import discord
import random 
import asyncio
import yt_dlp
from dotenv import load_dotenv
from discord.ext import commands
    

# Load environment variables
def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
# Intents
    intents = discord.Intents.default()
    intents.message_content = True  # Enables access to message content
# Bot command prefix
    bot = commands.Bot(command_prefix='*', intents=intents)
# voice client dictionary
    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
# ffmpeg options
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -filter:a "volume=0.1"'
        }
    current_volume = 0.1


# ---- Client events section ----
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has become a d e g e n...')
        print(f'Logged in as {bot.user}!')
        
    #  command not going to be called by any discord commands
    @bot.command(name='playNext')
    async def play_next(ctx):
        if queues[ctx.guild.id] != []:
            link = queues[ctx.guild.id].pop(0) #removes the end and holds it in a variable for link
            await play(ctx, link)
            await ctx.send("hey... i liked that one.... you ASS!!!! who gave you the Bluetooth??!! your taste is shit, jump off a bridge |.|-|.|Ne")
        
    #  this is to play in the server and make sure not every instance of a bot is being initiated everytime we type it
    @bot.command(name='play')
    async def play(ctx, link):
        try:
            if ctx.guild.id not in voice_clients:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client
            else:
                voice_client = voice_clients[ctx.guild.id]
        except Exception as error:
            print(error)
            
    # this is so the voice client isnt reset everytime we type 'play'
        try: 
            loop = asyncio.get_event_loop()
            # we dont want to download anything and we want to async run the loop 
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False)) 
            song_url = data['url'] # data is a json response
            player = discord.FFmpegOpusAudio(song_url, **ffmpeg_options)
            #labmda functions are 1 liners we dont have to define elsewhere in python... or anywhere actually
            # Play the audio
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
            await ctx.send(f"uWu playing: '{data['title']}' for my Darling!! >.<")
        except Exception as error:
            print(error)
            await ctx.send(f"i cant play that stupid!!  {error}")
            
    #setting the volume so i dont blow eardrums out........ 
    @bot.command(name='setVolume', help="im not yelling... (0.0 to 1.0)")
    async def set_volume(ctx, volume: float):
        global current_volume
        if 0.0 <= volume <= 1.0:
            current_volume = volume
            ffmpeg_options['options'] = f'-vn -filter:a "volume={current_volume}"'
            await ctx.send(f"You cant just turn me up or down!! there its at {volume * 100}% ...im not your ro-bitch you kno!!")
        else:
            await ctx.send("be realistic! betweenn 0.0 and 1.0. dipshit.... god do i have to tell you how to do E V E R Y T H I N G????!!!")
            
# play functionalities--------
    @bot.command(name='skip')
    async def skip(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await play_next(ctx)
            await ctx.send(f'you skipped my favorite song >:l')
        except Exception as error:
            print(error)
        
    
    @bot.command(name='clear')
    async def clear(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send(f'I cleared your queue darling...')
        else:
            await ctx.send('nothin to clear tho...')
    
    @bot.command(name='pause')
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
            await ctx.send(f"Darling you paused it, i was gettin down >.>")
        except Exception as error:
            print(error)
            
    @bot.command(name='resume')
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
            await ctx.send(f"yeahhh!! back in business >:D")
        except Exception as error:
            print(error)
            
    @bot.command(name='stop')
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
            await ctx.send(f"great! now im never gonna dance again!!! >:O")
        except Exception as error:
            print(error)
            

    @bot.command(name="queue")
    async def queue(ctx, url):
        if ctx.guild.id not in  queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(url)
        await ctx.send("another one eh... ^....( '.')> ")

# ---- Bot events section ------------

    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'ARA ARA {bot.user.name} welcomes you to the shit show :D!'
        )

    @bot.event
    async def on_error(event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

# Command to respond with a philosophical quote when 'darling' is typed
    @bot.command(name='darling', help='responds with words you might never hear...')
    async def darling(ctx):
        philisophicalQuotes = [
            'If you don’t belong here, just build a place where you do.',
            'If you don’t have a partner, find one.\nif you can’t, take one by force!!!',
            'It doesn’t matter how long it takes, \nas long as we have souls, \nI’m sure I will meet you again',
            'you know, no one can swim in the same river water twice. \nWe must choose our own path...',
            'Maybe we can\'t win alone, but the two of us together can!',
            'You\'re my baby boi arent you ;)',
            'I\'m always alone, too. Thanks to these circuits...',
            '... can we just lie here for a bit...',
            'wanna run away with me? I can get you out of here.',
            'If you have anything you wanna say to someone, you better spit it out while you can. Because you\'re going to die sooner or later... darling...',
            'Don’t worry darling... We’ll always be together until we die.',
            (
                'The distant skies... Beyond time...\n'
                'what an overwhelmingly long journey just for the two of us... wouldnt you say?\n'
                'I\'ll remember your warmth, along with the memories we\'ve made together...\n' 
            ),
            (
                'If you place your hopes in anything, they will be betrayed.\n' 
                'Promises will go unfulfilled, and faith will let you down...'
            ),
            (
                'I read an old book that said what it means love each other...\n' 
                'I want to inherit that bond.'
            ),
            (   
                'If I look up, I see thousands of lives shining deep in the sky. \n' 
                'So far away and although I try, I just can\'t reach out...\n'
                'Yet, even with broken wings, we\'ll fly away once again... right darling?'
            ),
            (
                'without you... \n'
                'leaving something behind... \n' 
                'My body can\'t do that....'
            ), 
        ]
        response = random.choice(philisophicalQuotes)
        await ctx.send(response)

#easter egg... 
    @bot.command(name='be_safe', aliases=['be...safe...'], help='heheheheh')
    async def be_safe(ctx):
        stay = [
            'Stay Dangerous!....',
            '... i will...'
        ]
        response = random.choice(stay)
        await ctx.send(response)

# dice game---------
    @bot.command(name='dice', help='I wanna go gambling muffin...\n Type the number of dice you want to roll...\n now the number of sides the dice have...\n it should look like this - *dice 2 6\n that means you want to roll two six sided dice :)')
    async def roll(ctx, number_dice: int, number_sides: int):
        dice = [
            str(random.choice(range(1, number_sides + 1)))
            for _ in range(number_dice)
        ]
        await ctx.send(f'you rolled a: {" , ".join(dice)} ... ha! weak!!!')
    
# creating a channel
    @bot.command(name='create-channel')
    @commands.has_role('Admin')
    async def create_channel(ctx, channel_name: str='meh'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
            await ctx.send(f'Bout time you did something around here... >.> `{channel_name}` <.< !')
        else:
            await ctx.send(f'`{channel_name}` already exists, be more creative...')
        
# error handling for creating a channel
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('but.. but... you arent an admin... T.T')
        else:
            await ctx.send(f'there you go typing nonsense again *.* {str(error)}')

# --------- End bot events section ---------

# Run the bot with the token
    bot.run(TOKEN)
