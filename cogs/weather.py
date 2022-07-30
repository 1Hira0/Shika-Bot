from io import BytesIO
from PIL import Image, ImageDraw
import nextcord, requests, os
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

weatherapi_key = os.environ['e'].replace("'", "")
weather_url = "http://api.weatherapi.com/v1"
weather_reqs = {"Current weather":"current.json", 
                "Forecast":"forecast.json"}


class Weather(commands.Cog):
    def __init__(self, client): self.client = client
    
    @nextcord.slash_command(name="weather")
    async def weather(ctx:Interaction): ...

    @weather.subcommand(name='current',description='Current Weather')
    async def current(self, ctx:Interaction, location:str=SlashOption(description="location/IP address/long,lat")):
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
    
    @weather.subcommand(name='forecast', description='Forecast for the day')
    async def fr(self, ctx:Interaction, location:str=SlashOption(description="location/IP address/long,lat")):
        response = (requests.get(f"{weather_url}/{weather_reqs['Forecast']}?key={weatherapi_key}&q={location}"))
        print(response.status_code, "\n")
        r = response.json()

        if response.status_code == 200:
            place = r['location']
            forecast = r['forecast']['forecastday'][0]
            if forecast['day']['daily_chance_of_rain'] == 0 : rain = ""
            else: rain = f"\nChances of raining: {forecast['day']['daily_chance_of_rain']}"
            if forecast['day']['daily_chance_of_snow'] == 0: snow = "" 
            else: snow = f"\nChances of snowing: {forecast['day']['daily_chance_of_snow']}"
            emb = nextcord.Embed(description=f"""Max temperature : {forecast['day']['maxtemp_c']}℃ {forecast['day']['maxtemp_f']}℉ \nMin temperature: {forecast['day']['mintemp_c']}℃ {forecast['day']['mintemp_c']}℉ \nWind speed: {forecast['day']['maxwind_kph']}kph {rain} \nHumidity: {forecast['day']['avghumidity']}% {rain} {snow} \nSun: Rise - {forecast['astro']['sunrise']} Set - {forecast['astro']['sunset']} \nMoon: Rise - {forecast['astro']['moonrise']} Set - {forecast['astro']['moonset']}""")
            emb.set_author(name=f"Forecast of {forecast['date']} in {place['name']}, {place['region']}, {place['country']}")
            
            await ctx.send(embed=emb)
            img1 = Image.open('BLACK.png')
            imgs = [Image.open(BytesIO(requests.get(f"https:{hour['condition']['icon']}").content)) for hour in r['forecast']['forecastday'][0]['hour']]

            for i in range(24):
                myc, myr, myt= i, 0, 60
                if i > 11: myc, myr, myt = i-12, 70, 130
                img2 = ImageDraw.Draw(img1)
                img2.text((myc*70 +16,myt), r['forecast']['forecastday'][0]['hour'][i]['time'][10:], (255,255,255))
                img1.paste(imgs[i], (myc*70,myr), mask = imgs[i])
            img1 = img1.crop((0,0,840,140))
            emb.set_image(img1)
            img1.save('forecast.png')
            file = nextcord.File("forecast.png", filename="forecast.png")
            emb.set_image(url="attachment://forecast.png")
            await ctx.edit_original_message(embed=emb)

def setup(client): client.add_cog(Weather(client))