import discord
from discord.ext import commands

class Remove(commands.Cog):
  def __init__(self, client):
	  self.client = client
	
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    print(member)
    server = member.guild
    welcome_channel = discord.utils.get(server.channels, name="welcome") 
    if welcome_channel == None:
      welcome_channel = server.system_channel
    await welcome_channel.send(f"{member.name} has left {server.name}")
		
def setup(client):
	client.add_cog(Remove(client))