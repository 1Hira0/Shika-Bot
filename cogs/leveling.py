from nextcord.ext import commands
<<<<<<< Updated upstream
import math, nextcord

class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):        
        if self.client.user in ctx.mentions: await ctx.channel.send("https://tenor.com/view/anime-gif-18020020", delete_after=4.75)
        elif False:#((ctx.guild.id == 722858994170986527) and (ctx.author.id == 159985870458322944 or ctx.author.id == 602098932260143124) and ("GG!" in ctx.content[:3])): # FOR THE BONGS237 SERVER            member = ctx.mentions[0]
            mee6 = [int(s) for s in str.split(ctx.content) if s.isdigit()]
            print(mee6)
            print("mee6[0]%10","\n", mee6[0]%10)
            roles = [
            758006690254684201, #potato              - 01
            868194728536047697, #cooked potato       - 02
            868196256835579985, #raw sweet potato    - 03
            868196448188125254, #cooked sweet potato - 04
            868196661535600700, #an old potato       - 05
            896441917682888755, #bronze potato       - 06
            896442494269657188, #Silver Potato       - 07
            896442687400595487, #Golden Potato       - 08
            896442965256446062, #Diamond Potato      - 09
		    896443470108053514] #Veteran Potato      - 10
            if not(mee6[0]%10 == 0): return
            chan = self.client.get_channel(932301921346261092)
            chosen = roles[math.floor(mee6[0]/10)]
            print(ctx.guild)
            role = ctx.guild.get_role(chosen)
            await member.add_roles(role)
            msg = f"Member:{member} \nServer:{ctx.guild} \nLVL:{mee6} \nQuetient: {mee6[0]/10}, THE NUMBER: {math.floor(mee6[0]/10)} \nTHE CHOSEN: {chosen} \nRole given to {member.mention}, Role:{role.name}"
            print(msg)
            await chan.send(embed=nextcord.Embed(description=msg)) 
def setup(client): client.add_cog(Levels(client))
=======
import math, nextcord, requests, os
from random import choice


habitica_userKeys = requests.post("https://habitica.com/api/v3/user/auth/local/login?", data={"username":"1Hira0", "password":os.environ['1Hira0']}).json()
headers = {"x-api-user":habitica_userKeys['data']['id'], "x-api-key":habitica_userKeys['data']['apiToken']}

gifs = {'https://tenor.com/view/clown-nightmare-clowns-scary-horror-gif-19977226'                              : 4.3, 
		"https://tenor.com/view/creepy-bubble-gum-chewing-scary-face-gif-17178119"                             : 4.5,
		"https://tenor.com/view/tank-engine-meme-scaring-memes-gif-19928134"                                   : 3.72, 
		"https://tenor.com/view/abell46s-reface-miedo-creepy-creepy-smile-gif-18969229"                        : 3.9, 
		"https://tenor.com/view/sysk-stuff-you-should-know-josh-clark-creepy-hands-human-octopus-gif-12904827" : 3, 
		"https://tenor.com/view/creepy-scary-gif-24535133"                                                     : 4.2,
	    "https://tenor.com/view/horror-thomas-the-tank-engine-ttte-creepy-weird-gif-14485153"                  : 7.91, 
		"https://tenor.com/view/smiling-cat-creepy-cat-cat-zoom-kitty-gif-18136879"                            : 1.8, 
		"https://tenor.com/view/black-dark-scary-spooky-creepy-face-gif-16729560"                              : 9.8, 
		"https://tenor.com/view/split-tongue-creepy-snapchat-mouth-eyes-gif-14516121"                          : 4.51, 
		"https://tenor.com/view/lick-face-tongue-out-flat-face-gif-15917217"                                   : 7.52, 
		"https://tenor.com/view/eyes-creepy-halloween-make-up-gif-13260717"                                    : 1.1, 
		"https://tenor.com/view/star-wars-chewbacca-upset-screaming-screaming-scream-gif-22135921"             : 1.99,
	    "https://tenor.com/view/this-is-what-youre-doing-this-is-what-i-want-you-to-do-gif-19589141"           : 5}

my_gifs = list(gifs.keys())

class Miscellaneous(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, ctx):        
		if self.client.user in ctx.mentions:
			global my_gifs, gifs
			my_gif = choice(my_gifs)

			await ctx.channel.send(content=my_gif, delete_after=gifs[my_gif])        
		elif ctx.content.lower() == "ikr"  and ctx.author.id == 968057839820079194:
			await ctx.delete()        
		elif False: #((ctx.guild.id == 951344945762013195) and (ctx.author.id == 159985870458322944 or ctx.author.id == 602098932260143124) and (f"{ctx.content}".startswith('GG!'))):
			member = ctx.mentions[0]
			mee6 = [int(s) for s in str.split(ctx.content) if s.isdigit()]
			print(mee6)
			print("mee6[0]%5","\n", mee6[0]%5)
			if mee6[0] < 5: 
				chan = self.client.get_channel(970310321724084314)
				chosen = 972074928738287637
				print(ctx.guild)
				role = ctx.guild.get_role(chosen)
				await member.add_roles(role)
				msg = f"Member:{member} \nServer:{ctx.guild} \nLVL:{mee6} \nQuetient: {mee6[0]/5}, THE NUMBER: {math.floor(mee6[0]/10)} \nTHE CHOSEN: {chosen} \nRole given to {member.mention}, Role:{role.name}"
				print(msg)
				await chan.send(embed=nextcord.Embed(description=msg))
				return
			roles = [
					972074928738287637,
					972075752302469171,
					972075698690867221,
					972075809248534528,
					972075842354167818,
					972075894837485689,
					972075931856424981] 
			if not(mee6[0]%5 == 0): return
			chan = self.client.get_channel(970310321724084314)
			chosen = roles[math.floor(mee6[0]/5)]
			print(ctx.guild)
			role = ctx.guild.get_role(chosen)
			await member.add_roles(role)
			msg = f"Member:{member} \nServer:{ctx.guild} \nLVL:{mee6} \nQuetient: {mee6[0]/5}, THE NUMBER: {math.floor(mee6[0]/5)} \nTHE CHOSEN: {chosen} \nRole given to {member.mention}, Role:{role.name}"
			print(msg)
			await chan.send(embed=nextcord.Embed(description=msg)) 


	@nextcord.slash_command(name="msg_habitca", description='Sends message to habitca', guild_ids=[867720161351565333])
	async def send_h(self, ctx, content:str): requests.post("https://habitica.com/api/v3/groups/party/chat", data={"message":content}, headers=headers)
	
def setup(client): client.add_cog(Miscellaneous(client))
>>>>>>> Stashed changes
