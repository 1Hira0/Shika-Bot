from keep_alive import keep_alive
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord, requests, os, math, asyncio, datetime


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
    description="Name of the anime"
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
    print("search used")
    r = requests.get(url=f"{mal_url}/anime?q={anime}&limit={limit}", headers=headers)
    print(r.status_code, f"\n{r.url}")
    if r.status_code == 200:
        r_dict = r.json()['data']
        text = "\n".join([f"{i+1}. {r_dict[i]['node']['title']}" for i in range(len(r_dict))])
        print(f"\n'{text}'\n")
        emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=f"Search results for {anime}", 
		url=f"https://myanimelist.net/search/all?q={anime}&cat=all", 
		icon_url="https://replit.com/@Hira10/Shika#mal_icon.png"
        )
        await ctx.response.send_message(embed=emb)
    elif r.status_code!= 400: 
        await ctx.response.send_message(content=f"Not found '{anime}'", ephemeral=True)


@anime.subcommand(name="info", description=("anime info"))
async def info(ctx:Interaction, name:str=animeSl_name):
    anime  = requests.get(url=f"{mal_url}/anime?q={name}&limit={5}", headers=headers)
    r = anime.json()['data']
    text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(anime.json()['data']))])
    print(text)
    emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
    emb.set_author(name=f"For {name}"
	, url=f'https://myanimelist.net/search/all?q={name.replace(" ", "%20")}&cat=all', 
		#, 
		#icon_url="https://replit.com/@Hira10/Shika#mal_icon.png"
        )
    emb.set_footer(text=f"Not in here? Tap on the title to open MyAnimelist")
    await ctx.response.send_message(embed=emb)
    message = await ctx.original_message()
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")
    
    def check(reaction, user):
        return user == ctx.user and str(reaction.emoji) in ["1️⃣","2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    try:
        reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
        if   str(reaction.emoji) == "1️⃣": chosen = 0
        elif str(reaction.emoji) == "2️⃣": chosen = 1
        elif str(reaction.emoji) == "3️⃣": chosen = 2
        elif str(reaction.emoji) == "4️⃣": chosen = 3
        elif str(reaction.emoji) == "5️⃣": chosen = 4
        else: await message.remove_reaction(reaction, user)
        try:
            await message.clear_reactions()
        except nextcord.errors.Forbidden:
            print("no perms")
    except asyncio.TimeoutError:
        chosen = 0
		
    if anime.status_code == 200:
        print(anime.json())
        animeID = anime.json()['data'][chosen]['node']['id']
        response = requests.get(url=f"{mal_url}/anime/{animeID}?fields=title,main_picture,start_date,end_date,synopsis,mean,rank,nsfw,created_at,status,genres,num_episodes,average_episode_duration,recommendations,studios",  headers=headers)
        r = response.json()
        nsfw = ""
        if r['nsfw'] != 'white': nsfw = "\nnfsw"
        ep_num = f"{r['num_episodes']} episode"
        if r['num_episodes'] < 2: ep_num = f"{ep_num}s"
        synp = r['synopsis'].replace('\n\n','\n')
        time_needed = f"{math.floor((r['num_episodes'] * r['average_episode_duration'])/3600)} hours {((r['num_episodes'] * r['average_episode_duration'])//60)%60} minutes"
        genre = ", ".join([i['name'] for i in r['genres']])
        if r['recommendations']:
            recom = ",\n".join([r['recommendations'][i]['node']['title'] for i in range(2)])
        else: recom = "None"
        studio = r['studios'][0]['name']
        if "end_date" in r :timing = f"\nfrom {r['start_date']} to {r['end_date']}"
        else: timing = f"\nfrom {r['start_date']} to ?(airing)"
        msg = f"{synp} \n\nStudio: {studio} \n⭐:{r['mean']} ||  🏆: {r['rank']}th \n{genre} \n{ep_num} \ntotal run time: {time_needed} \nsimilar: {recom} {nsfw} {timing}"
        emb= nextcord.Embed(description=msg, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=r['title'], icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png",
		url= f"https://myanimelist.net/anime/{animeID}")
        emb.set_footer(text="Want more info? Tap on the title to open it on MyAnimelist")
        emb.set_thumbnail(url=r['main_picture']['large'])
        await message.edit(embed=emb)
        print(msg)
    else:await ctx.response.send_message(content='Not found', ephemeral=True)
animeSl_limit.description='limit of anime'
animeSl_limit.max_value = 500
animeSl_limit.default = 20
cho = {
		"Top Anime Series"       :'all'         ,
		"Top Airing Anime"       :'airing'      ,
		"Top Upcoming Anime"     :'upcoming'    ,
		"Top Anime TV Series"    :'tv'          ,
		"Top Anime OVA Series"   :'ova'         ,
		"Top Anime Movies"       :'movie'       ,
		"Top Anime Specials"     :'special'     ,
		"Top Anime by Popularity":'bypopularity',
		"Top Favorited Anime"    :'favorite'    
		}
animeSl_ranks=SlashOption(
	name="type",
	description='Type of ranking',
	required=True,
	choices=cho
 )

def get_key(val):
    for key, value in cho.items():
         if val == value:
             return key
 
    return "key doesn't exist"


@anime.subcommand(name='ranking', description='Anime ranking')
async def rank(ctx: Interaction, _type:str=animeSl_ranks, limit:int=animeSl_limit):
    ranking = requests.get(f'{mal_url}/anime/ranking?ranking_type={_type}&limit={limit}', headers=headers)
    title = get_key(_type)
    print(ranking.status_code)
    if ranking.status_code == 200:
        r = ranking.json()['data']
        contents = []
        for i in range(int(len(r)/10)): 
            contents.append("\n".join([f"{((i*10)+j)+1}. {r[(i*10)+j]['node']['title']}" for j in range(10)]))
        pages = len(contents)
        cur_page = 1
        emb=nextcord.Embed(description=contents[cur_page-1], color=nextcord.Color(0x2E51A2))
        emb.set_author(name=title, url=f'https://myanimelist.net/topanime.php?type={_type}', 
				#, 
		#icon_url="https://replit.com/@Hira10/Shika#mal_icon.png"
        )
        emb.set_footer(text=f"Page {cur_page}/{pages}")
        message = await ctx.response.send_message(embed=emb)
        if message is None: message = await ctx.original_message()

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.user and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    emb.description=contents[cur_page-1]
                    emb.set_footer(text=f"Page {cur_page}/{pages}")
                    await ctx.edit_original_message(embed=emb)
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    emb.description=contents[cur_page-1]
                    emb.set_footer(text=f"Page {cur_page}/{pages}")
                    await ctx.edit_original_message(embed=emb)
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break

#animeSl_year = SlashOption(name="year", required=True, min_value=1965, #max_value=datetime.date.today().year, default=datetime.date.today().year, #autocomplete=True)
#animeSl_season = SlashOption()
#@anime.subcommand(name="seasonal", description="Season's anime")
#async def seasonal(ctx:Interaction, animeSl_year, animeSl_season, #animeSl_limit):
#	response = requests.get(url=f"#{mal_url}/anime/season/{animeSl_year}/{animeSl_season}?limit={animeSl_limit}")
#	if response.status_code == 200:
#		r = response.json()



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