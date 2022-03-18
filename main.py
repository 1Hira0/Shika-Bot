from keep_alive import keep_alive
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord, requests, os, math, asyncio, time

weatherapi_key = os.environ['e'].replace("'", "")
weather_url = "http://api.weatherapi.com/v1"
weather_reqs = {"Current weather":"current.json", 
        "Forecast":"forecast.json"}

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

@client.slash_command(name="ping", description="sends bot latency")
async def ping(ctx:Interaction): await ctx.response.send_message(f"Ping: {round(client.latency *1000)}ms")


@client.slash_command(name="weather")
async def weather(ctx:Interaction): ...

@weather.subcommand(name='current',description='Current Weather')
async def current(ctx:Interaction, location:str=SlashOption(description="location/IP address/long,lat")):
    response = (requests.get(f"{weather_url}/{weather_reqs['Current weather']}?key={weatherapi_key}&q={location}"))
    print(response.status_code, "\n")
    r = response.json()

    if response.status_code == 200:
        place = r['location']
        now = r['current']

        temperature = f"\ntemperature: {now['temp_c']}℃ {now['temp_f']}℉"
        weather_cond = f"\n{now['condition']['text']} "
        cond_icon = now['condition']['icon'][2:]
        if now['wind_kph'] > 15: wind_kph = f"\nwind speed: {now['wind_kph']} kpmh"
        else:wind_kph=""  
        if now['precip_mm'] > 0:precip = f"\n amount of rain: {now['precip_mm']}mm"
        else:precip = ''
        humidity = f"\nhumidity: {now['humidity']}%"
        cloud = f"\ncloudiness: {now['cloud']}%"
        current_weather = f"{weather_cond}{temperature}{wind_kph}{humidity}{cloud}{precip}"
        tempColor = nextcord.Color.green()
        if now['temp_c'] > 30: tempColor = nextcord.Color.red()
        elif now['temp_c'] < 10: tempColor = nextcord.Color.blue()
        embed = nextcord.Embed(
                title=f"Current weather at `{place['name']}, {place['region']}, {place['country']}`", description=current_weather, color=tempColor) 
        embed.set_thumbnail(url="https://"+cond_icon)
        embed.set_author(name=f"{place['localtime'][10:]} in {place['country']}")
        embed.set_footer(text=f"last updated at: `{now['last_updated']}`")

        await ctx.response.send_message(embed=embed)
    else:
        print(r)
        await ctx.response.send_message(content=f"{r['error']['message']} For {location}", ephemeral=True)

@client.slash_command(name="test", description="testing")
async def test(ctx:Interaction): await ctx.response.send_message(embed=nextcord.Embed(title="test", description="testing done"))
keep_alive()
client.run(os.environ['env'])