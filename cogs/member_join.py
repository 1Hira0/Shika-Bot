import nextcord 
from nextcord.ext import commands
with open("./speshal servs/income.txt", "r") as f:
	income = (f.read())
class Join(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
     if str(member.guild.id) in income: 
      return None
      print(member)
      server = member.guild
      welcome_channel = nextcord.utils.get(server.channels, name="welcome") 
      if welcome_channel == None:
         welcome_channel = server.system_channel
      await welcome_channel.send(f"<@!{member.id}> has joined {server.name}")

def setup(client):
	client.add_cog(Join(client))