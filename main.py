from keep_alive import keep_alive
from nextcord import Interaction
from nextcord.ext import commands
import nextcord, os, time


client = commands.Bot(command_prefix="%")

@client.event
async def on_ready(): print(f"{client.user} has joined the game")

#loading commands from folders
@client.command()
async def load(ctx, extension):
	if str(ctx.author.id) == "602098932260143124":
			client.load_extension(f"cogs.{extension}")
			print(f"loaded {extension} at {time.ctime()}")
			await ctx.channel.send(f"loaded {extension} at {time.ctime()}")
	else:await ctx.send("You can't use that")

#reloading commands from folders
@client.command()
async def reload(ctx, extension):
	if str(ctx.author.id) == "602098932260143124":
			client.reload_extension(f"cogs.{extension}")
			print(f"reloaded {extension} at {time.ctime()}")
			await ctx.channel.send(f"reloaded {extension} at {time.ctime()}")
	else:await ctx.send("You can't use that")

#unloading commands from folders
@client.command()
async def unload(ctx, extension):
	msg = f"unloaded {extension} at {time.ctime()}"
	if str(ctx.author.id) == "602098932260143124":
			client.unload_extension(f"cogs.{extension}")
			print(msg)
			await ctx.channel.send(msg)
	else:await ctx.send("You can't use that")
 
#finding command-files and loading them
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")


@client.slash_command(name="test", description="testing")
async def test(ctx:Interaction): await ctx.response.send_message(embed=nextcord.Embed(title="test", description="testing done"))
keep_alive()
client.run(os.environ['env'])