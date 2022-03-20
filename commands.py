import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class Allcommands(commands.Cog):
    def __init__(self, client): self.client = client
    
    @commands.slash_command(name="ping", description="sends bot latency")
    async def ping(self, ctx:Interaction): await ctx.response.send_message(f"Ping: {round(self.client.latency *1000)}ms")

def setup(client): client.add_cog(Allcommands(client))