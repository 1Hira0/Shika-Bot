from nextcord.ext import commands
import math, nextcord

class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):        
        if self.client.user in ctx.mentions: await ctx.channel.send("https://tenor.com/view/anime-gif-18020020", delete_after=4.75)
        elif False:#((ctx.guild.id == 722858994170986527) and (ctx.author.id == 159985870458322944 or ctx.author.id == 602098932260143124) and ("GG!" in ctx.content[:3])): # FOR THE BONGS237 SERVER -https://discord.gg/ardVCeZ
            member = ctx.mentions[0]
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
