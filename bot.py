import discord
from discord.ext import commands
import wavelink

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await wavelink.Pool.connect(
        cls=wavelink.Node,
        host='lava.link',
        port=80,
        password='youshallnotpass',
        bot=bot,
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await ctx.voice_client.disconnect() if ctx.voice_client else None
        await channel.connect(cls=wavelink.Player)
        await ctx.send(f"Joined {channel.name}")
    else:
        await ctx.send("You must be in a voice channel.")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command("join"))

    tracks = await wavelink.YouTubeTrack.search(search, return_first=True)
    vc: wavelink.Player = ctx.voice_client
    await vc.play(tracks)
    await ctx.send(f"Now playing: {tracks.title}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected.")

bot.run("YOUR_BOT_TOKEN")
