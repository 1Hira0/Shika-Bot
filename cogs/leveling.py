from discord.ext import commands
import math, discord

class Levels(commands.Cog):
   def __init__(self, client):
      self.client = client

   @commands.Cog.listener()
   async def on_message(self, ctx):
      if ctx.channel.id == 904590281540771840: # FOR GAMER'S PARADISE - https://discord.com/invite/ckPHDTgT2c
         member = ctx.mentions[0]
         mee6 = [int(s) for s in str.split(ctx.content) if s.isdigit()]
         roles = [
         876032522008535041, 
         890513662870163456, 
         930806878081011772, 
         930807278121132072, 
         930807278121132072]
         if not(mee6[0]%5 == 0): return
         chan = self.client.get_channel(930776729650348073)
         chosen = roles[math.floor(mee6[0]/5)]
         role = ctx.guild.get_role(chosen)
         await member.add_roles(role)
         try:
            await member.remove_roles(ctx.guild.get_role(roles[math.floor(mee6[0]/5)-1]))
         except IndexError as error:
            await chan.send(error)
         msg = f"Member:{member} \nServer:{ctx.guild} \nLVL:{mee6} \nQuetient: {mee6[0]/5}, THE NUMBER: {math.floor(mee6[0]/5)} \nTHE CHOSEN: {chosen} \nRole given to {member.mention}, Role:{role.name}"
         print(msg)
         await chan.send(embed=discord.Embed(description=msg)) 
         oldnick = member.nick
         if oldnick == None:
            oldnick = member.name
         elif oldnick != None and any(lvlname in oldnick for lvlname in ["wood", "stone", "iron" ,"gold", "diamond"]):
            rolename, nick = oldnick.split("|")
            print(rolename, nick)
            oldnick = nick
         newnick = f"{role.name} | {oldnick}"
         await member.edit(nick=newnick)
            
      elif ctx.guild.id == 722858994170986527 and (ctx.author.id == 159985870458322944 or ctx.author.id == 602098932260143124) and ("GG!" in ctx.content[:3]): # FOR THE BONGS237 SERVER -https://discord.gg/ardVCeZ
         member = ctx.mentions[0]
         mee6 = [int(s) for s in str.split(ctx.content) if s.isdigit()]
         print(mee6)
         roles = [758006690254684201, #potato - 1
         868194728536047697, #cooked potato - 2
         868196256835579985, #raw sweet potato - 3
         868196448188125254, #cooked sweet potato - 4
         868196661535600700, #an old potato - 5
         896441917682888755, #bronze potato - 6
         896442494269657188, #Silver Potato - 7
         896442687400595487, #Golden Potato - 8
         896442965256446062, #Diamond Potato - 9
				 896443470108053514] #Veteran Potato - 10
         if not(mee6[0]%10 == 0): return
         chan = self.client.get_channel(932301921346261092)
         chosen = roles[math.floor(mee6[0]/10)]
         print(ctx.guild)
         role = ctx.guild.get_role(chosen)
         await member.add_roles(role)
         msg = f"Member:{member} \nServer:{ctx.guild} \nLVL:{mee6} \nQuetient: {mee6[0]/10}, THE NUMBER: {math.floor(mee6[0]/10)} \nTHE CHOSEN: {chosen} \nRole given to {member.mention}, Role:{role.name}"
         print(msg)
         await chan.send(embed=discord.Embed(description=msg)) 




         
def setup(client):
    client.add_cog(Levels(client))
