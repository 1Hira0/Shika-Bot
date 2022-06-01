import asyncio
import datetime
import math
import os
from io import BytesIO

import nextcord
import requests
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from PIL import Image

from mangareader import get_mangareader

thisyear = datetime.date.today().year

mal_url = 'https://api.myanimelist.net/v2'
headers = {'Authorization': f"Bearer {os.environ['mal']}"}
auth = {'X-MAL-CLIENT-ID':f"{os.environ['clientid']}"}


def make_gif(pictures):
    frames = [Image.open(BytesIO(requests.get(url=image['medium']).content)) for image in pictures]
    frame_one = frames[0]
    frame_one.save("manga.gif", format="GIF", append_images=frames,
               save_all=True, duration=1000, loop=0)
    return "manga.gif"

cho = {
    "Top Anime Series"       :'all'         ,
    "Top Airing Anime"       :'airing'      ,
    "Top Upcoming Anime"     :'upcoming'    ,
    "Top Anime TV Series"    :'tv'          ,
    "Top Anime OVA Series"   :'ova'         ,
    "Top Anime Movies"       :'movie'       ,
    "Top Anime Specials"     :'special'     ,
    "Top Anime by Popularity":'bypopularity',
    "Top Favorited Anime"    :'favorite'    }

cho2 = {
    "All"           :"all"         ,
    "Top Manga"     :"manga"       ,
    "Top Novels"    :"novels"      ,
    "Top One-shots" :"oneshots"    ,
    "Top Doujinshi" :"doujin"      ,
    "Top Manhwa"    :"manhwa"      ,
    "Top Manhua"    :"manhua"      ,
    "Most Popular"  :"bypopularity",
    "Most Favorited":"favorite"}

animeSl_limit=SlashOption(
        name="limit",
        default=5,
        required=False, 
        min_value=1, max_value=20, 
        description="Amount of search results")

def get_key(val):
    global cho
    for key, value in cho.items():
        if val == value:
             return key
        return "key doesn't exist"

class Anime(commands.Cog):
    
    def __init__(self, client): self.client = client

    @nextcord.slash_command(name="anime")
    async def anime(self, ctx:Interaction): ...
    animeSl_name=SlashOption(
        name="anime",
        description="Name of the anime"
    )
    @anime.subcommand(
        name="search", description="Search for anime"
    )
    async def search(self, ctx:Interaction, anime:str=animeSl_name, limit:int=animeSl_limit):
        print("search used")
        r = requests.get(url=f"{mal_url}/anime?q={anime}&limit={limit}", headers=auth)
        print(r.status_code, f"\n{r.url}")
        if r.status_code == 200:
            r_dict = r.json()['data']
            text = "\n".join([f"{i+1}. {r_dict[i]['node']['title']}" for i in range(len(r_dict))])
            print(f"\n'{text}'\n")
            emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"Search results for {anime}", 
    		url=f"https://myanimelist.net/search/all?q={anime}&cat=all", 
    		icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
            )
            emb.set_footer(text="Want more info? Tap on the menu to see more information")
            await ctx.response.send_message(embed=emb)
        elif r.status_code!= 400: 
            await ctx.response.send_message(content=f"Not found '{anime}'", ephemeral=True)
    
    
    @anime.subcommand(name="info", description=("anime info"))
    async def info(self, ctx:Interaction, name:str=animeSl_name):
        anime  = requests.get(url=f"{mal_url}/anime?q={name}&limit={5}", headers=auth)
        r = anime.json()['data']
        text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(anime.json()['data']))])
        print(text)
        emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=f"For {name}",
    	               url=f'https://myanimelist.net/search/all?q={name.replace(" ", "%20")}&cat=all', 
    		           icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
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

            animeID = anime.json()['data'][chosen]['node']['id']
            response = requests.get(url=f"{mal_url}/anime/{animeID}?fields=title,main_picture,start_date,end_date,synopsis,mean,rank,nsfw,created_at,status,genres,num_episodes,average_episode_duration,recommendations,studios",  headers=auth)
            r = response.json()
            print(r)
            #nsfw shit
            nsfw = ""
            if r['nsfw'] != 'white': nsfw = "\nnfsw"
            #number of episode(s)
            ep_num = f"\n{r['num_episodes']} episode"
            if r['num_episodes'] < 2: ep_num = f"{ep_num}s"
            #description of show
            synp = r['synopsis'].replace('\n\n','\n')
            #total time needed to complete the show (calulated from avg. time,in sec, for one ep - given from MAL )
            time_needed = f"\ntotal run time: {math.floor((r['num_episodes'] * r['average_episode_duration'])/3600)} hours {((r['num_episodes'] * r['average_episode_duration'])//60)%60} minutes"
            if ' 0 hours 0 minutes' in time_needed : time_needed = ''
            print(time_needed)
            #genre of the show
            genre = ''
            if 'genres' in r :genre = f"\n{', '.join([i['name'] for i in r['genres']])}"
            else: genre = '\ngenre: Not available yet'
            #recommendation/relatable shows
            recom = ''
            if r['recommendations']:recom +=  "\nsimilar: "+(',\n'.join([r['recommendations'][i]['node']['title'] for i in range(len(r['recommendations']))]))
            #studio which made this show
            studio = ''
            if r['studios'] :studio += f"\n\nStudio: {r['studios'][0]['name']}"
            #start & end date of release/ airing/ not released
            if r['status'] == 'not_yet_aired':timing = "\nNot aired yet"
            elif r['status'] == 'currently_airing': timing = f"\nfrom {r['start_date']} to ?(airing)"
            elif r['status'] == 'finished_airing':timing = f"\nfrom {r['start_date']} to {r['end_date']}"
            #rank on MAL
            ranga = '' #ranga is a character from Tensei Slime Datta Ken (That Time I Got Reincarnated as a Slime)
            if 'rank' in r: 
                if   str(r['rank']).endswith('1'): ranga = f"🏆: {r['rank']}st"
                elif str(r['rank']).endswith('2'): ranga = f"🏆: {r['rank']}nd"
                elif str(r['rank']).endswith('3'): ranga = f"🏆: {r['rank']}rd"
                else: ranga = f"🏆: {r['rank']}th"
            else: ranga = 'Not ranked yet'
            avg = 'Not scored yet'
            if 'mean' in r: avg=f"\n⭐:{r['mean']}"
            msg = f"{synp} {studio} {avg} ||  {ranga} {genre} {ep_num} {time_needed} {recom} {nsfw} {timing}"
            emb= nextcord.Embed(title=r['title'], description=msg, color=nextcord.Color(0x2E51A2), url= f"https://myanimelist.net/anime/{animeID}")
            emb.set_author(name="Tap here to play", icon_url="https://animixplay.to/favicon.ico",
    		url= f"https://animixplay.to/anime/{animeID}")
            emb.set_footer(text="Want more info? Tap on the title to open it on MyAnimelist", icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
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
        ranking = requests.get(f'{mal_url}/anime/ranking?ranking_type={_type}&limit={limit}', headers=auth)
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
    		#icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
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


class Manga(commands.Cog):
    def __init__(self, client): self.client = client
		
    @nextcord.slash_command(name="manga", description="manga")
    async def manga(self, ctx:Interaction): ...
    mangaSl_name=SlashOption(
        name="manga",
        description="Name of the manga")
    animeSl_limit.default=5,
    animeSl_limit.max_value=20
    @manga.subcommand(
        name="search", description="Search for manga")
    async def mangasearch(self, ctx:Interaction, manga:str=mangaSl_name, limit:int=animeSl_limit):
        print("search used")
        r = requests.get(url=f"{mal_url}/manga?q={manga}&limit={limit}", headers=auth)
        print(r.status_code, f"\n{r.url}")
        if r.status_code == 200:
            r_dict = r.json()['data']
            text = "\n".join([f"{i+1}. {r_dict[i]['node']['title']}" for i in range(len(r_dict))])
            print(f"\n'{text}'\n")
            emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
            emb.set_author(name=f"Search results for {manga}", 
    		url=f"https://myanimelist.net/search/all?q={manga}&cat=all", 
    		icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
            )
            await ctx.response.send_message(embed=emb)
        elif r.status_code == 400: 
            await ctx.response.send_message(content=f"Not found '{manga}'", ephemeral=True)
        
        
    @manga.subcommand(name="info", description=("Information on a manga"))
    async def mangainfo(self, ctx:Interaction, name:str=mangaSl_name):
        manga  = requests.get(url=f"{mal_url}/manga?q={name}&limit={5}", headers=auth)
        r = manga.json()['data']
        text = "\n".join([f"{i+1}. {r[i]['node']['title']}" for i in range(len(manga.json()['data']))])
        print(text)
        emb=nextcord.Embed(description=text, color=nextcord.Color(0x2E51A2))
        emb.set_author(name=f"For {name}"
    	, url=f'https://myanimelist.net/search/all?q={name.replace(" ", "%20")}&cat=all', 
    		#, 
    		#icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
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
            try:await message.clear_reactions()
            except nextcord.errors.Forbidden:print("no perms")
        except asyncio.TimeoutError:chosen = 0
        
        if manga.status_code == 200:
            print(manga.json())
            mangaID = manga.json()['data'][chosen]['node']['id']
            response = requests.get(url=f"{mal_url}/manga/{mangaID}?"+"fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization",  headers=auth)
            r = response.json()
            creators = "\n"+"\n".join([f"{author['role']} by {author['node']['first_name']} {author['node']['last_name']}" for author in r['authors']])
            titles = r['alternative_titles']['synonyms'] + [r['alternative_titles']['en'], r['title'], r['alternative_titles']['ja']]
            pirate = get_mangareader(r['title'])
            reading = [tit for tit in titles if tit in pirate.keys()][0]
            #description of manga
            synp = r["synopsis"].replace("\n\n", "\n")
            #rank of manga
            genre = ''
            if 'genres' in r :genre = f"\n{', '.join([i['name'] for i in r['genres']])}"
            else: genre = '\ngenre: Not available yet'
            #recommendation/relatable mangas
            recom = ''
            
            lee = len(r['recommendations'])
            if lee >5:lee = 5
            if r['recommendations']:recom +=  "\nsimilar: "+(',\n'.join([r['recommendations'][i]['node']['title'] for i in range(lee)]))
            #rank on MAL
            ranga = '' #ranga is a character from Tensei Slime Datta Ken (That Time I Got Reincarnated as a Slime)
            if 'rank' in r: 
                ranga = f"🏆: {r['rank']}"
                if   str(r['rank']).endswith('1'): f"{ranga}st"
                elif str(r['rank']).endswith('2'): f"{ranga}nd"
                elif str(r['rank']).endswith('3'): f"{ranga}rd"
                else: ranga = f"{ranga}th"
            else: ranga = 'Not ranked yet'
            #score of manga on MAL
            avg = ''
            if 'mean' in r: avg=f"\n⭐:{r['mean']}"
            else:avg = 'Not scored yet'
            #status + chapters + publishing dates
            chapters = f"\nNo. of chapter(s): {r['num_chapters']}"
            if r['status'] == 'currently_publishing': 
                r['title'] = f"{r['title']} (currently publishing)"
                chapters = "\nChapter count isn't available while publishing"
                pub_dates = f"\nPublishing since {r['start_date']}"
            if 'serialization' in r: serialIn = f"\nSerialised in {r['serialization'][0]['node']['name']}"
            else:serialIn = ""
            print(reading)
            msg = f"{synp} \n{avg} || {ranga} {creators} {chapters} {pub_dates} {serialIn} {genre} {recom} "
            emb= nextcord.Embed(title=r['title'], description=msg, color=nextcord.Color(0x2E51A2), url= f"https://myanimelist.net/manga/{mangaID}")
            emb.set_author(name="Read at", icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png", url=pirate[reading])
            emb.set_footer(text="Want more info? Tap on the title to open it on MyAnimelist", icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
            emb.set_thumbnail(url=r['main_picture']['large'])
            make_gif(r['pictures'])
            emb.set_image("""https://cdn.myanimelist.net/images/manga/3/80661.jpg""")
            await message.edit(embed=emb)
            print(msg)
        else:await ctx.response.send_message(content='Not found', ephemeral=True)
        
    animeSl_limit.description='limit of manga'
    animeSl_limit.max_value = 500
    animeSl_limit.default = 20
    animeSl_ranks=SlashOption(
    	name="type",
    	description='Type of ranking',
    	required=True,
    	choices=cho
    )
        
    @manga.subcommand(name='ranking', description='Manga ranking')
    async def ranks(self, ctx: Interaction, _type:str=animeSl_ranks, limit:int=animeSl_limit):
        ranking = requests.get(f'{mal_url}/manga/ranking?ranking_type={_type}&limit={limit}', headers=auth)
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
            emb.set_author(name=title, url=f'https://myanimelist.net/topmanga.php{_type}', 
    				#, 
    		#icon_url="https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
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
userName = SlashOption(name='username', description="User's MAL username", required=True)
userStatus = SlashOption(name='status', description="User's anime status in MAL", required=False, choices={"All":"",  "Watching":"&status=watching",  "Completed":"&status=compleyed",  "On-hold":"&status=on_hold",  "Dropped":"&status=dropped", "PTW":"&status=plan_to_watch"}, default="")
class User(commands.Cog):
    def __init__(self, client): self.client = client
    
    @nextcord.slash_command(name="user")
    async def user(self, ctx:Interaction):...
    
    @user.subcommand(name="animelist", description="User's animelist")
    async def animelist(self, ctx:Interaction, username:str=userName, listStat:str=userStatus):
        response = requests.get(url=f"{mal_url}/users/{username}/animelist?limit=1000{listStat}&sort=list_updated_at", headers=headers)
        
def setup(client): 
	client.add_cog(Manga(client))
	client.add_cog(Anime(client))
