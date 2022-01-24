from keep_alive import keep_alive
import discord, random, asyncio, os, time
from discord import FFmpegPCMAudio
from discord.ext import commands

intents = discord.Intents.all()

print("file running")

bot = commands.Bot(command_prefix=commands.when_mentioned_or('%'), intents=intents)
bot.remove_command("help")
#removing the inbuilt help command
owner = '639259314074157077'
master = '602098932260143124'
mastwo =  '847861640833007686'
discEpoch = 1420070400000


with open("./speshal servs/powerfuls.txt", "r") as f:
	powerfuls =f.read()



@bot.command()
async def appendPowerfuls(ctx, memberID:int):
	if str(ctx.author.id) in powerfuls:
		with open("./speshal servs/powerfuls.txt", "a") as fi:
			fi.append(memberID)



@bot.command()
async def appendServer(ctx, serverID: int):
	with open("./speshal servs/income.txt", "a") as f:
		f.append(serverID)



@bot.event
async def on_ready(): #when the bot comes online
		print(f'{bot.user} has joined the game!')
	


powerful = ["powerful"]
@bot.command(aliases=powerful)
async def supercum(ctx, *,com): 
    print(com)
    if str(ctx.author.id) in powerfuls: 
        exec(com)
        await ctx.channel.send(f"executed the following command ```py\n{com}\n```")



# THE COMMANDS
# THE HELP COMMAND - discord.ext adds an in-built help command and this is an extra help command
@bot.command()
async def help(ctx, cummand=None):
	if cummand == None:
		await ctx.channel.send(embed=discord.Embed(title="Shika's commands", description="""Hello my name is Shika, Japanese for Hira\n
		My Prefix is `%`
		These are my functions: 
			`%slap` - slaps a `target` 
			`%ping` - sends my latency 
			`%help` this msg where my master tried to be funny, please forgive me, i didnt do anything wrong! 
			`%hug` lets you hug `target`
			`%rps(Rock Paper Scissors)` - Play's Rock Paper Scissors with you ||maybe between player in the future too!||
			`%avatar` - sends the user's avatar"""))
		await ctx.channel.send(embed=discord.Embed(title="Commands in development",description="`Songs/Lyrics`(very unsure and may take more than 6 months), `Image to Ascii` "))
		await ctx.channel.send("Use the command name after `%help` for more info into the command")
	
	elif cummand != None:
		#more info for slap command
		if "slap" in cummand:
			await ctx.channel.send("The slap command lets you send an virtual slap to 	someone.\nIt requires a target to slap!")
			await ctx.channel.send(file=discord.File("slap.png"))

		#more info for ping command
		elif "ping" in cummand:
			await ctx.channel.send("The ping command sends how long it takes for the bot 	to respond to a message")
			await ctx.channel.send(file=discord.File("ping.png"))

		#more info for the help command itself
		elif "help" in cummand:
			await ctx.channel.send(f"The help command sends the list of commands for 	{bot.user} which is manually edited")
			await ctx.channel.send(file=discord.File("help.png"))
	
		#more info for hug command
		elif "hug" in cummand:
			await ctx.channel.send("The hug command lets you send online hugs to someone 	else.\nIt requires a target to send the hugs to!")
			await ctx.channel.send(file=discord.File("hug.png"))

		#more info for checkAV command
		elif "av" in cummand or "pfp" in cummand or "avatar" in cummand:
			await ctx.channel.send("Use 	`%checkAV`, this sends the avatar of a person.\n %checkAV `optional(user-id 	or mention)`")
			await ctx.channel.send(file=discord.File("checkAV.png"))

		#more info for songs
		elif "song" in cummand or "music" in cummand or "anime" in cummand or "rand" in 	cummand: 
			songs = os.listdir("./songs")
			songslist1 = "\n".join([f"{i+1}. {songs[i]}" for i in range(10)])
			songslist2 = "\n".join([f"{i+11}. {songs[i+10]}" for i in range(10)])
			songslist3 = "\n".join([f"{i+20}. {songs[i+20]}" for i in range(9)])
			contents = [songslist1.replace(".mp3",""), songslist2.replace(".mp3",""), 	songslist3.replace(".mp3","")]
			contents[0] = contents[0].title()
			contents[1] = contents[1].title()
			contents[2] = contents[2].title()
			pages = len(contents)
			cur_page = 1
			message = await ctx.channel.send(f"```\nPage {cur_page}/{pages}:\n{contents	[cur_page-1]} \n```")

			await message.add_reaction("◀️")
			await message.add_reaction("▶️")

			def check(reaction, user):
					return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

			while True:
					try:
							reaction, user = await bot.wait_for("reaction_add", timeout=60, 	check=check)
							if str(reaction.emoji) == "▶️" and cur_page != pages:
									cur_page += 1
									await message.edit(content=f"```\nPage {cur_page}/{pages}:\n	{contents[cur_page-1]}\n```")
									await message.remove_reaction(reaction, user)

							elif str(reaction.emoji) == "◀️" and cur_page > 1:
									cur_page -= 1
									await message.edit(content=f"```\nPage {cur_page}/{pages}:\n	{contents[cur_page-1]}\n```")
									await message.remove_reaction(reaction, user)

							else:
									await message.remove_reaction(reaction, user)
					except asyncio.TimeoutError:
							break

		elif "special" in cummand:
			await ctx.channel.send("`%supercum` \n`%load` \n`%unload")

	print("Help was ran")



#loading commands from folders
@bot.command()
async def load(ctx, extension):
	if str(ctx.author.id) in powerfuls:
			bot.load_extension(f"commands.{extension}")
			print(f"loaded {extension} at {time.ctime()}")
			await ctx.channel.send(f"loaded {extension} at {time.ctime}")
	else:
		await ctx.send("You can't use that")

#reloading commands from folders
@bot.command()
async def reload(ctx, extension):
	if str(ctx.author.id) in powerfuls:
			bot.reload_extension(f"commands.{extension}")
			print(f"reloaded {extension} at {time.ctime()}")
			await ctx.channel.send(f"reloaded {extension} at {time.ctime()}")
	else:
		await ctx.send("You can't use that")


#unloading commands from folders
@bot.command()
async def unload(ctx, extension):
	msg = f"unloaded {extension} at {time.ctime()}"
	if str(ctx.author.id) in powerfuls:
			bot.unload_extension(f"commands.{extension}")
			print(msg)
			await ctx.channel.send(msg)
	else:
		await ctx.send("You can't use that")



#finding command-files and loading them
for filename in os.listdir("./commands"):
	if filename.endswith(".py"):
		bot.load_extension(f"commands.{filename[:-3]}")



#
#@bot.command()
#async def remove_welcome(ctx):
	


# THE SLAP COMMAND
@bot.command(aliases=["hit","smack"])
async def slap(message, *targ):
	target = " ".join([f"{targ[i]}" for i in range(len(targ))])
	slapper = message.author.mention
	all_slaps = ["slapped", "smacked", "hit"]
	slaps = random.choice(all_slaps)
	print("Slap was ran")
	print("Target spotted",target)
	print("Assilant spotted",slapper)
	if owner in target:
			print("Someone tried to slap Bongs")
			if slapper == owner:
					print("Bongs tried to slap himslef")
					await message.channel.send("Don't hurt yourself majesty")
			elif slapper != owner:
					print("Someone else tried to slap Bongs")
					await message.channel.send("No one slaps the Potato King!")
	elif master in target or mastwo in target:
			await message.channel.send("You are not allowed to slap daddy!")
			
	elif str(message.author.id) in target:
			await message.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target},but regret hurting themself"))
		
	elif "790123597246889994" in target:
			await message.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target}"))
			await message.channel.send("I am sad now :pensive:")

	elif not(owner in target) and not(master in target) and not(mastwo in target) and not(str(message.author.id) in target):
			await message.channel.send(embed=discord.Embed(description=f"{slapper} {slaps} {target}"))



# THE HUG COMMAND
@bot.command()
async def hug(message, *,target):
  member_ping = message.author.mention
  huggie = random.choice(["hugs", "gives a big hug to", ":people_hugging:"])
  print("Hug was ran")
  print(target)
  await message.channel.send(embed=discord.Embed(description=f"{member_ping} {huggie} {target}"))
  if member_ping in target:
    await message.channel.send(embed=discord.Embed(description=message.author.mention + " tries to hug themself, realises that they are lonely and becomes sad"))
    await message.channel.send("Oh don't be sad!  " )
    await message.channel.send(embed=discord.Embed(description=f"<@!790123597246889994> {huggie} {member_ping}"))
    return
  elif "<@!790123597246889994>" in target or "<@790123597246889994>" in target:
    print("Someone hugged me, YAY!")
    await message.channel.send('Oh thank you!')
    await message.channel.send(embed=discord.Embed(description=f'<@!790123597246889994> hugs {member_ping}  back'))



# THE PING COMMAND
@bot.command(aliases=["latency"])
async def ping(ctx):
		start_time = (ctx.message.id >> 22) + discEpoch
		ping_message = await ctx.channel.send("Checking ping! :ping_pong:")
		end_time = (ping_message.id >> 22) + discEpoch
		await ping_message.edit(content=f'Websocket: {round(bot.latency*1000)}ms | RoundaBout {end_time-start_time}ms')



# THE AVATAR COMMAND 
@bot.command(aliases=["av", "pfp", "avatar", "profile picture"])
async def checkAV(ctx, adult_video : discord.Member=None): #here adult_video is a pun for AV as an abbreviation for adult video
	if adult_video != None:
		pfp = adult_video.avatar_url_as(static_format="png", size=4096)
		print(pfp)
		await ctx.channel.send(pfp)
	elif adult_video == None:
		await ctx.channel.send(ctx.author.avatar_url_as(static_format="png", size=4096))



# THE JOIN(VOICE CHANNEL) COMMAND (in development)
@bot.command(aliases=["connect","vc"], name="join")
async def join(ctx):
	await ctx.channel.send("This command is in development. You may encounter **errors!**. ")
	channel = ctx.author.voice.channel
	await channel.connect()
	await ctx.channel.send(embed=discord.Embed(title="VC ativity", description="Joined VC"))



# THE PLAY COMMAND (in development)
@bot.command(aliases=["song", "rand","random","randsong"])
async def play(ctx, *,newsong=None):
	await ctx.channel.send("This command is in development. You may encounter **errors!**")
	music_dir = "./songs"
	if newsong == None: 
		song = random.choice(os.listdir(music_dir))
	elif not(newsong == None):
		song = newsong.lower() + ".mp3"
	the_file = os.path.join(music_dir, song)
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice == None:
		voice = await ctx.author.voice.channel.connect()
	voice.play(FFmpegPCMAudio(the_file))
	await bot.change_presence(activity=discord.Activit(type=discord.ActivityType.listening, name=(song.replace(".mp3","")).title())) #this changes the status



# THE LEAVE COMMAND (in development)
@bot.command(aliases=["disconnect", "fuck off", "get out", "bye"])
async def leave(ctx):
	if str(ctx.author.id) in powerfuls:
	    server = ctx.guild.voice_client
	    await server.disconnect()


#for i in ["music.py", "ToAscii.py"]: bot.unload_extension(f"commands.{i}")


keep_alive()

bot.run(os.environ['env'])