import discord
from discord.ext import commands, tasks
import os
import random

with open('token.txt', 'r') as file:
    TOKEN = file.read()

FKK_CHANNEL_ID = 942191175975190528
AFK_CHANNEL_ID = 848348815861743616

AUDIO_FOLDER = 'audio'

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)


def getRandomAudioFile():
    audio_files = os.listdir(AUDIO_FOLDER)
    return AUDIO_FOLDER + '/' + random.choice(audio_files)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    channel = bot.get_channel(FKK_CHANNEL_ID)
    if channel:
        print(f'Bot will play audio in channel: {channel.name}')
        play_audio.start(channel)
    else:
        print(f'Channel with ID {FKK_CHANNEL_ID} not found. Please check the channel ID.')


@tasks.loop(seconds=1)
async def play_audio(channel):
    voice_channel = discord.utils.get(bot.voice_clients, guild=channel.guild)

    if voice_channel is None or not voice_channel.is_connected():
        voice_channel = await channel.connect()

    if not voice_channel.is_playing():
        voice_channel.play(discord.FFmpegPCMAudio(getRandomAudioFile()),
                           after=lambda e: print(f'Error: {e}') if e else None)


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == AFK_CHANNEL_ID:
        # Replace 'TARGET_CHANNEL_ID' with the ID of the channel where you want to move the user
        target_channel = bot.get_channel(FKK_CHANNEL_ID)

        if target_channel:
            await member.move_to(target_channel)
            print(f'{member.name} moved from {after.channel.name} to {target_channel.name}')
        else:
            print(f'Target channel with ID {FKK_CHANNEL_ID} not found. Please check the channel ID.')


@bot.event
async def on_disconnect():
    play_audio.stop()


bot.run(TOKEN)
