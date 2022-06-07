import nextcord, asyncio, random, os
from nextcord import Interaction, FFmpegPCMAudio, SlashOption
from nextcord.ext import commands 



discEpoch = 1420070400000

class AllCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # THE HELP COMMAND - nextcord.ext adds an in-built help command and this is an extra help command
    @commands.command()
    async def help(self, ctx, *,cummand=None):
        if cummand == None:
            await ctx.channel.send(embed=nextcord.Embed(title="Shika's commands", description="""Hello my name is Shika, Japanese for Hira\n
My Prefix is `%`
    These are my functions: 
        `%slap` - slaps a `target` 
        `%ping` - sends my latency 
        `%help` this msg where my master tried to be funny, please forgive me, i didnt do anything wrong! 
        `%hug` lets you hug `target`
        `%rps(Rock Paper Scissors)` - Play's Rock Paper Scissors with you ||maybe between player in the future too!||
        `%avatar` - sends the user's avatar
        `%toascii` - changes uploaded image to ascii (urls don't work for now and images are required)
        /anime: `search` - search results for the name provided,
        	    `info` - info for specified anime,
                ``
        		``"""))

            await ctx.channel.send(embed=nextcord.Embed(title="Possible commands in future",description="`Songs/Lyrics`(very unsure and may take more than 6 months), MAL(MyAnimeList) implementation(notifications for new shows and checking out shows)-in Dev-slash command, weather forecasting-in Dev-slash command"))
            await ctx.channel.send("Use the command name after `%help` for more info into the command")

        elif cummand != None:
        	#more info for slap command
            if "slap" in cummand:
                await ctx.channel.send("The slap command lets you send an virtual slap to 	someone.\nIt requires a target to slap!")
                await ctx.channel.send(file=nextcord.File("./help images/slap.png"))

        	#more info for ping command
            elif "ping" in cummand:
                await ctx.channel.send("The ping command sends how long it takes for the bot 	to respond to a message")
                await ctx.channel.send(file=nextcord.File("./help images/ping.png"))

            #more info for the help command itself
            elif "help" in cummand:
                await ctx.channel.send(f"The help command sends the list of commands for 	{self.client.user} which is manually edited")
                await ctx.channel.send(file=nextcord.File("./help images/help.png"))

            #more info for hug command
            elif "hug" in cummand:
                await ctx.channel.send("The hug command lets you send online hugs to someone 	else.\nIt requires a target to send the hugs to!")
                await ctx.channel.send(file=nextcord.File("./help images/hug.png"))

            #more info for checkAV command
            elif "av" in cummand or "pfp" in cummand or "avatar" in cummand:
                await ctx.channel.send("Use 	`%checkAV`, this sends the avatar of a person.\n %checkAV `optional(user-id 	or mention)`")
                await ctx.channel.send(file=nextcord.File("./help images/av.png"))

            #more info for songs
            elif "song" in cummand or "music" in cummand or "rand" in cummand: 
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
                        reaction, user = await self.client.wait_for("reaction_add", timeout=60, 	check=check)
                        if str(reaction.emoji) == "▶️" and cur_page != pages:
                            cur_page += 1
                            await message.edit(content=f"```\nPage {cur_page}/{pages}:\n	{contents[cur_page-1]}\n```")
                            await message.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "◀️" and cur_page > 1:
                            cur_page -= 1
                            await message.edit(content=f"```\nPage {cur_page}/{pages}:\n	{contents[cur_page-1]}\n```")
                            await message.remove_reaction(reaction, user)

                        else:await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError: 
                        await message.remove_reactions()
                        break

            elif "ascii" in cummand: 
                await ctx.channel.send("`%toascii`: **image file required**, turns image into ascii", file=nextcord.File("./help images/toascii.png"))
            
            elif "special" in cummand:
                await ctx.channel.send("`%powerful` \n`%load` \n`%unload")
            
            elif "anime" in cummand or "weather" in cummand: 
                ctx.channel.send("")
        await ctx.channel.send("Due to migration from nextcord.py to nextcord there can be some error")

        print("Help was ran")
    
    @nextcord.slash_command(name="ping", description="sends bot latency")
    async def ping(self, ctx:Interaction):
        start_time = (ctx.message.id >> 22) + discEpoch
        await ctx.response.send_message("Checking ping! :ping_pong:")
        ping_message = await ctx.original_message()
        end_time = (ping_message.id >> 22) + discEpoch
        await ctx.edit_original_message(content=f'Websocket: {round(self.client.latency*1000)}ms | RoundaBout {end_time-start_time}ms')

    # THE AVATAR COMMAND 
    @nextcord.slash_command(name="avatar", description="sends avatar")
    async def checkAV(self, ctx:Interaction, 
                      adult_video : nextcord.Member=SlashOption(
                            name="member", description="member mention/ID", 
                            required=False, autocomplete=True)
                      ): #here adult_video is a pun for AV as an abbreviation for adult video
        if adult_video != None:
            await ctx.response.send_message(adult_video.avatar_url(size=4096))
        elif adult_video == None:
            await ctx.response.send_message(ctx.user.avatar_url(size=4096))

#	# THE PLAY COMMAND (in development)
#    @commands.command(aliases=["song", "rand","random","randsong"])
#    async def play(self, ctx, *,newsong=None):
#        await ctx.channel.send("This command is in development. You may encounter **errors!**")
#        music_dir = "./songs"
#        if newsong == None: 
#            song = random.choice(os.listdir(music_dir))
#        elif not(newsong == None):
#            song = newsong.lower() + ".mp3"
#        the_file = os.path.join(music_dir, song)
#        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
#        if voice == None:
#            voice = await ctx.author.voice.channel.connect()
#        voice.play(FFmpegPCMAudio(the_file))
#        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=(song.replace(".mp3","")).title())) #this changes the status

def setup(client): client.add_cog(AllCommands(client))