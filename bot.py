import discord
from discord.ext import commands
import wavelink
import os
import imageio_ffmpeg

# Set FFmpeg path
os.environ["PATH"] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + os.pathsep + os.environ["PATH"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await wavelink.NodePool.connect(
        client=bot,
        nodes=[
            wavelink.Node(uri="http://lava.link:80", password="youshallnotpass")
        ]
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You need to be in a voice channel!")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command("join"))

    vc: wavelink.Player = ctx.voice_client
    track = await wavelink.YouTubeTrack.search(search, return_first=True)
    await vc.play(track)
    await ctx.send(f"Now playing: {track.title}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")
    else:
        await ctx.send("I'm not connected to a voice channel.")

# Use environment variable for security
bot.run(os.getenv("BOT_TOKEN"))
