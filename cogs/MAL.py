import nextcord, os, requests, asyncio, math, datetime
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

thisyear = datetime.date.today().year

mal_url = 'https://api.myanimelist.net/v2'
headers = {'Authorization': f"Bearer {os.environ['mal']}"}

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

def get_key(val):
    global cho
    for key, value in cho.items():
        if val == value:
             return key
        return "key doesn't exist"

class Anime(commands.Cog):
    
    def __init__(self, client): self.client = client

    @commands.slash_command(name="anime")
    async def anime(self, ctx:Interaction): ...
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
    async def search(self, ctx:Interaction, anime:str=animeSl_name, limit:int=animeSl_limit):
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
    async def info(self, ctx:Interaction, name:str=animeSl_name):
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
            reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
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
    animeSl_ranks=SlashOption(
    	name="type",
    	description='Type of ranking',
    	required=True,
    	choices=cho
    )
    
    
    @anime.subcommand(name='ranking', description='Anime ranking')
    async def rank(self, ctx: Interaction, _type:str=animeSl_ranks, limit:int=animeSl_limit):
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
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
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
    animeSl_limit.max_value = 100
    animeSl_year = SlashOption(name="year", description="year of anime release", required=True, min_value=1965, max_value=thisyear, default=thisyear)
    animeSl_season = SlashOption(name="season", description="season of anime release", required=True, choices=["Current", "Winter", "Fall", "Summer", "Spring"], default="Current")
    @anime.subcommand(name='season', description='Anime of seasons')
    async def seasonal(self, ctx:Interaction, year:int=animeSl_year, season:str=animeSl_season, limit:int=animeSl_limit):
        response = requests.get(url=f"{mal_url}/anime/season/{year}/{season}?limit={limit}")
        if response.status_code == 200:
            r_dict = response.json()
            print(r_dict)
            contents = []
            for i in range(int(len(r_dict['data'])/10)): 
                try:
                    contents.append("\n".join([f"{((i*10)+j)+1}. {r_dict['data'][(i*10)+j]['node']['title']}" for j in range(10)]))
                except IndexError: print("something happened")
            pages = len(contents)
            cur_page = 1
            emb=nextcord.Embed(description=contents[cur_page-1], color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"{r_dict['season']['season'].capitalize()} {r_dict['season']['year']}", 
                           url=f"https://myanimelist.net/anime/season/{r_dict['season']['year']}/{r_dict['season']['season']}",  
                           icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
            emb.set_footer(text=f"Page {cur_page}/{pages} | click on the title for more info")
            message = await ctx.response.send_message(embed=emb)
            if message is None: message = await ctx.original_message()
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")
            def check(reaction, user):
                return user == ctx.user and str(reaction.emoji) in ["◀️", "▶️"]
            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        emb.description=contents[cur_page-1]
                        emb.set_footer(text=f"Page {cur_page}/{pages} | click on the title for more info")
                        await ctx.edit_original_message(embed=emb)
                        await message.remove_reaction(reaction, user)
                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        emb.description=contents[cur_page-1]
                        emb.set_footer(text=f"Page {cur_page}/{pages} | click on the title for more info")
                        await ctx.edit_original_message(embed=emb)
                        await message.remove_reaction(reaction, user)
                    else:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    break
                
def setup(client): client.add_cog(Anime(client))