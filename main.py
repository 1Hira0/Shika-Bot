from keep_alive import keep_alive
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord, requests, os

mal_url = 'https://api.myanimelist.net/v2'
headers = {'Authorization': f"Bearer {os.environ['mal']}"}

weatherapi_key = os.environ['e'].replace("'", "")
weather_url = "http://api.weatherapi.com/v1"
weather_reqs = {"Current weather":"current.json", 
        "Forecast":"forecast.json"}

client = commands.Bot(command_prefix="%")

@client.event
async def on_ready(): print(f"{client.user} has joined the game")


@client.slash_command(name="anime")
async def anime(ctx:Interaction): ...
animeSl_name=SlashOption(
    name="anime",
    description="Name/ID(mal id) of the anime"
)
animeSl_limit=SlashOption(
    name="limit",
    default=5,
    required=False, 
    min_value=1, max_value=20, 
    description="Amount of search results"
)
@anime.subcommand(
    name="search", description="Search for anime"
)
async def search(ctx:Interaction, anime:str=animeSl_name, limit:int=animeSl_limit):
    r = requests.get(url=f"{mal_url}/anime?q={anime}&limit={limit}", headers=headers)
    print(r.status_code, f"\n{r.url}")
    if r.status_code == 200:
        r_dict = r.json()['data']
        text = ("\n".join([f"{i+1}. {r_dict[i]['node']['title']}" for i in range(len(r_dict))])), r.status_code
    print(f"\n{anime}\n")
    if r.status_code == 200:
        embed=nextcord.Embed(title=f"Search results for {anime}",description=f"{text}")
        await ctx.response.send_message(embed=embed)
    elif r.status_code!= 400: 
        await ctx.response.send_message(content=f"Not found {r.status_code}", ephemeral=True)

#@anime.subcommand(
#		name="info", description=("anime info")
#)
#async def info(ctx:Interaction, anime:str=animeSl_name): ...







@client.slash_command(name="ping", description="sends bot latency")
async def ping(ctx:Interaction): await ctx.response.send_message(f"Ping: {client.latency *1000}ms")

@client.slash_command(name="weather")
async def weather(ctx:Interaction): ...

@weather.subcommand(name='current',description='Current Weather')
async def current(ctx:Interaction, location:str=SlashOption(description="location/IP address/long,lat")):
    r = (requests.get(f"{weather_url}/{weather_reqs['Current weather']}?key={weatherapi_key}&q={location}"))
    print(r.status_code, "\n")
    r_dict = r.json()

    if r.status_code == 200:
        place = r_dict['location']
        now = r_dict['current']

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

        embed = nextcord.Embed(
                title=f"Current weather at `{place['name']}, {place['region']}, {place['country']}`",
                description=current_weather) 
        embed.set_thumbnail(url="https://"+cond_icon)
        embed.set_author(name=f"{place['localtime'][10:]} in {place['country']}")
        embed.set_footer(text=f"last updated at: `{now['last_updated']}`")

        await ctx.response.send_message(embed=embed)
    else: 
        print(r_dict)
        await ctx.response.send_message(content=f"{r_dict['error']['message']} For {location}", ephemeral=True)


keep_alive()
client.run(os.environ['env'])