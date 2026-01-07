from discord.ext import commands
import discord
import CONFIG


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Hello! Winton is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Winton is now online!")
    
@bot.command()
async def add(ctx, x, y):
    result = int(x) + int(y)
    await ctx.send(f"The sum of {x} and {y} is {result}.")
    

bot.run(CONFIG.BOT_TOKEN)


