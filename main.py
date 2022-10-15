import discord 
from discord.ext import commands
import requests
import json 
from animals import Animals
import time
from datetime import datetime
import asyncio 
import random
import os 
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="?")

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity = discord.Game(name = "?help")) #technically doesn't belong here but still
    print("Bot is running!") #Yessir working

@bot.command(aliases = ["anim"])
async def animal(ctx, *, anim):
    animal = Animals(anim)
    await ctx.send(animal.fact())
    await ctx.send(animal.image())
@animal.error
async def animal_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an animal!")    

@bot.command(aliases = ["hi"])
async def hello(ctx):
    await ctx.send("Hello " f"{ctx.author.mention} <3 Hope you're having a good day!") #works

@bot.command()
async def love(ctx):
    await ctx.send("I love you too! <a:AG_BongoHeart:790239081551888434>")

@bot.command()
async def egg(ctx):
    await ctx.send(":egg:")

@bot.command()
@commands.has_permissions(ban_members = True)
async def purge(ctx , number : int):
    await ctx.channel.purge(limit = number + 1)
    await ctx.send(f"{number} messages purged!", delete_after = 3)
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions to execute the command.", delete_after = 3)
    

@bot.command()
async def hug(ctx , member : discord.Member):
    await ctx.send(f"{ctx.author.mention} has hugged {member.mention}!")
    await ctx.send("https://tenor.com/view/hug-anime-gif-11074788")

@bot.command()
@commands.has_permissions(ban_members = True)
async def whois(ctx, member : discord.Member ):
    embed = discord.Embed(title = member.name , description = member.mention , color = discord.Color.blue(), timestamp = datetime.utcnow())
    embed.add_field(name = "ID", value = member.id , inline = False)
    embed.add_field(name = "Joined on" , value = (member.joined_at.strftime("%m/%d/%Y at %H:%M:%S %p")) , inline = False )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url) 
    embed.add_field(name = "Roles", value = str(discord.Member.roles), inline = False) 
    embed.add_field(name = "Top role", value = member.top_role , inline = False)
    await ctx.send(embed = embed)
@whois.error
async def whois_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions to execute the command.", delete_after = 3)

@bot.event
async def on_member_join(member : discord.Member):
    await member.send(f'{member.name}, welcome to Periya Kudumbam!')

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title = "Liking me much?", color = 0x246a53)
    embed.add_field(name = "Hi!", value = (f"Hello {ctx.author}! You can invite me [here!](https://discord.com/api/oauth2/authorize?client_id=814972075071635477&permissions=0&scope=bot)"))
    await ctx.author.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ping(ctx):  
    msg3 = await ctx.send(f"{ctx.author.mention} Testing Ping...")
    await msg3.edit(content=f"{ctx.author.mention} pong! The ping took {round(bot.latency * 1000)} ms.")


@bot.command(aliases=["ar", "addrole"])
@commands.cooldown(rate=1, per=10.5, type=commands.BucketType.user)
@commands.has_permissions(manage_roles=True)
async def roleadd(ctx,  user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"`{role}` succesfully added to" f"<@{user.id}>""!")
@roleadd.error
async def roleadd_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You are on cooldown!")

@bot.command(aliases=["rr", "removerole"])
@commands.cooldown(rate=1, per=10.5, type=commands.BucketType.user)
@commands.has_permissions(manage_roles=True)
async def roleremove(ctx,  user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"`{role}` succesfully removed from" f"<@{user.id}>""!")
@roleremove.error
async def roleremove_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You are on cooldown!")

@bot.group(invoke_without_command = True)
async def help(ctx, * , command = None):
    await ctx.message.add_reaction("✅")
    embed = discord.Embed(title = "FelixBot help" , description = ("Use `?help <command>` for extra information on each function.") , color = 0xe74c3c , timestamp = datetime.utcnow())
    embed.add_field(name = "Moderation", value = "whois, purge, addrole, removerole", inline  = False)
    embed.add_field(name = "Astronomy", value = "apod, planet, hubble, position, iss, constellation, messier*", inline = False)
    embed.add_field(name = "Miscellaneous", value = "hello, love, animal, hug", inline = False)
    embed.set_footer(text = (f" Requested by {ctx.author}"), icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)
    


    
@bot.command(aliases = ["astronomy", "astropicture"])
@commands.cooldown(rate = 1, per = 10.5, type = commands.BucketType.user)
async def apod(ctx, date = None, ):
    try:
        if date == None or date == "today": #Not specifying date will automatically give the current day's picture
            picture = requests.get("https://api.nasa.gov/planetary/apod?api_key=96rc9TspKjyB1GjbGjIi3J0Ca3IY4NjxPN0ehAeJ").json()
            embed = discord.Embed(title = "Astronomy picture of the day", color = 0x57e051)
            embed.add_field(name = "Obtaining information from NASA", value = picture["explanation"])
            embed.set_image(url = picture["url"])
            embed.set_footer(text = f"Requested by {ctx.author} | APOD is updated once a day!")
            await ctx.send(embed = embed)
        elif date == "random":  #Picking a random date, avoided 2021 and 1995 to avoid uncecessary API errors and date is set to 28 because haha
            year = random.randint(1996, 2020)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            picture = requests.get(f"https://api.nasa.gov/planetary/apod?date={year}-{month}-{day}&api_key=96rc9TspKjyB1GjbGjIi3J0Ca3IY4NjxPN0ehAeJ").json()
            embed = discord.Embed(title = "Astronomy picture of the day", description = f"Showing picture for the day {year}-{month}-{day}", color = 0x57e051)
            embed.add_field(name = "Obtaining information from NASA", value = picture["explanation"])
            embed.set_image(url = picture["url"])
            embed.set_footer(text = f"Requested by {ctx.author} | APOD is updated once a day!")
            await ctx.send(embed = embed)
        else:  #This is for when the user inputs the actual date in the format YYYY-MM-DD
            picture = requests.get(f"https://api.nasa.gov/planetary/apod?date={date}&api_key=96rc9TspKjyB1GjbGjIi3J0Ca3IY4NjxPN0ehAeJ").json()
            embed = discord.Embed(title = "Astronomy picture of the day", description = None, color = 0x57e051)
            embed.add_field(name = "Obtaining information from NASA", value = picture["explanation"])
            embed.set_image(url = picture["url"])
            embed.set_footer(text = f"Requested by {ctx.author} | APOD is updated once a day!")
            await ctx.send(embed = embed)
     
    except KeyError: #Does commands.CommandInvokeError work? Should check later
        await ctx.send("Please enter a valid date! Time format supported is **YYYY-MM-DD**.")   
@apod.error
async def apod_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command is on cooldown!", delete_after = 3)

@bot.command()
async def iss(ctx):
    await ctx.send("Fetching ISS information...") #Is this really required? It's just to show off anyways
    iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    embed = discord.Embed(title = "ISS data!", description = "Displaying the ISS stats for the current time.", color = 0xbee3db, timestamp= datetime.utcnow())
    embed.set_image(url = "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/11/international_space_station/22293527-2-eng-GB/International_Space_Station_pillars.gif")
    embed.add_field(name = "Latitude", value = iss["latitude"], inline = True)
    embed.add_field(name = "Longitude", value = iss["longitude"], inline = True)
    embed.add_field(name = "Altitude", value = round(iss["altitude"], ndigits = 2), inline = False)
    embed.add_field(name = "Velocity", value = round(iss["velocity"], ndigits = 2), inline = True)
    embed.add_field(name = "Visibilty", value = iss["visibility"], inline = True)
    embed.set_footer(text = f"Requested by {ctx.author} | All values in kilometers")
    await ctx.send(embed = embed)


    
@bot.command()
@commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
async def planet(ctx, planet : str, simplified = "simplified"):
    planet_lowercase = planet.lower()  #doing this so that API error doesn't occur
    planet_list = ['http://space-facts.com/wp-content/uploads/mercury.png-transparent.png', #Lord forgive me for what I'm doing
    'http://space-facts.com/wp-content/uploads/venus-transparent.png', 
    'http://space-facts.com/wp-content/uploads/earth-transparent.png', 
    'http://space-facts.com/wp-content/uploads/mars-transparent.png', 
    'http://space-facts.com/wp-content/uploads/jupiter-transparent.png', 
    'http://space-facts.com/wp-content/uploads/saturn-transparent.png', 
    'http://space-facts.com/wp-content/uploads/uranus-transparent.png', 
    'http://space-facts.com/wp-content/uploads/neptune-transparent.png']
    
    if f"http://space-facts.com/wp-content/uploads/{planet_lowercase}-transparent.png" in planet_list:
        planet_picture = planet_list.index(f"http://space-facts.com/wp-content/uploads/{planet_lowercase}-transparent.png")
        url = planet_list[planet_picture]
    try:    
        if simplified == "advanced" or simplified == "adv": #That's a lot of information wewww that's why this isn't default
            planet_info = requests.get(f"https://api.le-systeme-solaire.net/rest/bodies/{planet_lowercase}").json()
            embed = discord.Embed(title = "Planet data", description = None, colour = 0x5dadf3)
            embed.add_field(name = "Name", value = planet_info["englishName"], inline = True)
            embed.add_field(name = "Semi-major axis", value = f"{planet_info['semimajorAxis']} kilometres", inline = False)
            embed.add_field(name = "Semi-minor axis", value = f"{planet_info['perihelion']} kilometres", inline = True)
            embed.add_field(name = "Aphelion", value = f"{planet_info['aphelion']} kilometres", inline = True)
            embed.add_field(name = "Inclination", value = f"{planet_info['inclination']}°", inline = False)
            embed.add_field(name = "Density", value = f"{planet_info['density']} kg/m³", inline = True)
            embed.add_field(name = "Gravitation", value = f"{planet_info['gravity']} m/s²" )
            mass = planet_info["mass"]
            embed.add_field(name = "Mass", value = f"{mass['massValue']}x 10^ {mass['massExponent']}kilograms", inline = False)
            embed.add_field(name = "Escape velocity", value = f"{planet_info['escape']} m/s", inline = True) 
            embed.add_field(name = "Sideral orbit period/length of year", value = f"{planet_info['sideralOrbit']} days", inline = False)
            embed.add_field(name = "Sideral rotation period/length of day", value = f"{planet_info['sideralRotation']} hours")
            embed.add_field(name = "Axial tilt", value = f"{planet_info['axialTilt']}°")
            embed.add_field(name= "Average temperature", value = f"{planet_info['avgTemp']}°C", inline = False )
            embed.add_field(name = "Mean radius", value = f"{planet_info['meanRadius']} kilometres")
            embed.set_image(url = url)
            embed.set_footer(text = f"Requested by {ctx.author}")
            await ctx.send(embed = embed)
            
        else:
            planet_info = requests.get(f"https://api.le-systeme-solaire.net/rest/bodies/{planet_lowercase}").json()
            embed2 = discord.Embed(title = "Planet data", description = None, colour = 0x5dadf3)
            embed2.add_field(name = "Name", value = planet_info["englishName"], inline = True)
            embed2.add_field(name = "Semi-major axis", value = f"{planet_info['semimajorAxis']} kilometres", inline = False)
            embed2.add_field(name = "Semi-minor axis", value = f"{planet_info['perihelion']} kilometres", inline = True)
            embed2.add_field(name = "Sideral orbit period/length of year", value = f"{planet_info['sideralOrbit']} days", inline = False)
            embed2.add_field(name = "Sideral rotation period/length of day", value = f"{planet_info['sideralRotation']} hours")
            embed2.set_image(url = url)           
            embed2.set_footer(text = f"Requested by {ctx.author}")
            await ctx.send(embed = embed2)

    except commands.CommandInvokeError:
        await ctx.send("Please enter the data correctly!")
@planet.error
async def planet_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command is on cooldown!", delete_after = 3) 
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Meow,* please enter the name of the planet!")   

@bot.command(aliases = ["av", "pfp"])
async def avatar(ctx, * , member : discord.Member):
    embed = discord.Embed(color = 0x5dadf3)
    embed.set_author(name = member.display_name)
    embed.set_image(url = member.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
@commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
async def visible(ctx, latitude : int, longitude : int):
    planets = requests.get(f"https://visible-planets-api.herokuapp.com/v2?latitude={latitude}&longitude={longitude}&showCoords=true").json()
    name = [] #Creating lists and appending each planet data because I'm dumb and this is the best fix I could think of
    ra = []
    dec = []
    for i in range(0, len(planets)):
        name.append(planets["data"][i]["name"])
        ra.append(planets["data"][i]["rightAscension"])
        dec.append(planets["data"][i]["declination"])

    try:
        embed = discord.Embed(title = "Planets visible", colour = 0xe5784a)
        for j in range(0, len(name)):
            embed.add_field(name = name[j], value = f"**RA**: {ra[j]['hours']} hours, {ra[j]['minutes']} minutes, {ra[j]['seconds']} seconds\n**DEC**: {dec[j]['degrees']}°, {dec[j]['arcminutes']}', {dec[j]['arcseconds']}'' ")
        embed.add_field(name = "Help",value = f"Confused about what RA and DEC are? Click [here.](http://spiff.rit.edu/classes/phys373/lectures/radec/radec.html)")
        await ctx.send(embed = embed)    

    except commands.MissingRequiredArgument:
        await ctx.send("Please enter latitude and longitude!")

@visible.error
async def visible_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command on cooldown!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Enter latitude and longitude!")

@bot.command()
@commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
async def constellation(ctx, * , constellation): #Do not open unless absolutely necessary as it's just 400 lines of JSON and ten lines of code
    constellations = [{                          
    "abbr": "And",
    "name": "Andromeda",
    "genitive": "Andromedae",
    "en": "Andromeda (mythological character)"
    
    }, {
    "abbr": "Ant",
    "name": "Antlia",
    "genitive": "Antliae",
    "en": "air pump"
    }, {
    "abbr": "Aps",
    "name": "Apus",
    "genitive": "Apodis",
    "en": "Bird-of-paradise"
    }, {
    "abbr": "Aqr",
    "name": "Aquarius",
    "genitive": "Aquarii",
    "en": "water-bearer"
    }, {
    "abbr": "Aql",
    "name": "Aquila",
    "genitive": "Aquilae",
    "en": "eagle"
    }, {
    "abbr": "Ara",
    "name": "Ara",
    "genitive": "Arae",
    "en": "altar"
    }, {
    "abbr": "Ari",
    "name": "Aries",
    "genitive": "Arietis",
    "en": "ram"
    }, {
    "abbr": "Aur",
    "name": "Auriga",
    "genitive": "Aurigae",
    "en": "charioteer"
    }, {
    "abbr": "Boo",
    "name": "Bo\u00f6tes",
    "genitive": "Bo\u00f6tis",
    "en": "herdsman"
    }, {
    "abbr": "Cae",
    "name": "Caelum",
    "genitive": "Caeli",
    "en": "chisel or graving tool"
    }, {
    "abbr": "Cam",
    "name": "Camelopardalis",
    "genitive": "Camelopardalis",
    "en": "giraffe"
    }, {
    "abbr": "Cnc",
    "name": "Cancer",
    "genitive": "Cancri",
    "en": "crab"
    }, {
    "abbr": "CVn",
    "name": "Canes Venatici",
    "genitive": "Canum Venaticorum",
    "en": "hunting dogs"
    }, {
    "abbr": "CMa",
    "name": "Canis Major",
    "genitive": "Canis Majoris",
    "en": "greater dog"
    }, {
    "abbr": "CMi",
    "name": "Canis Minor",
    "genitive": "Canis Minoris",
    "en": "lesser dog"
    }, {
    "abbr": "Cap",
    "name": "Capricornus",
    "genitive": "Capricorni",
    "en": "sea goat"
    }, {
    "abbr": "Car",
    "name": "Carina",
    "genitive": "Carinae",
    "en": "keel"
    }, {
    "abbr": "Cas",
    "name": "Cassiopeia",
    "genitive": "Cassiopeiae",
    "en": "Cassiopeia (mythological character)"
    }, {
    "abbr": "Cen",
    "name": "Centaurus",
    "genitive": "Centauri",
    "en": "centaur"
    }, {
    "abbr": "Cep",
    "name": "Cepheus",
    "genitive": "Cephei",
    "en": "Cepheus (mythological character)"
    }, {
    "abbr": "Cet",
    "name": "Cetus",
    "genitive": "Ceti",
    "en": "sea monster (whale)"
    }, {
    "abbr": "Cha",
    "name": "Chamaeleon",
    "genitive": "Chamaeleontis",
    "en": "chameleon"
    }, {
    "abbr": "Cir",
    "name": "Circinus",
    "genitive": "Circini",
    "en": "compasses"
    }, {
    "abbr": "Col",
    "name": "Columba",
    "genitive": "Columbae",
    "en": "dove"
    }, {
    "abbr": "Com",
    "name": "Coma Berenices",
    "genitive": "Comae Berenices",
    "en": "Berenice's hair"
    }, {
    "abbr": "CrA",
    "name": "Corona Australis",
    "genitive": "Coronae Australis",
    "en": "southern crown"
    }, {
    "abbr": "CrB",
    "name": "Corona Borealis",
    "genitive": "Coronae Borealis",
    "en": "northern crown"
    }, {
    "abbr": "Crv",
    "name": "Corvus",
    "genitive": "Corvi",
    "en": "crow"
    }, {
    "abbr": "Crt",
    "name": "Crater",
    "genitive": "Crateris",
    "en": "cup"
    }, {
    "abbr": "Cru",
    "name": "Crux",
    "genitive": "Crucis",
    "en": "southern cross"
    }, {
    "abbr": "Cyg",
    "name": "Cygnus",
    "genitive": "Cygni",
    "en": "swan or Northern Cross"
    }, {
    "abbr": "Del",
    "name": "Delphinus",
    "genitive": "Delphini",
    "en": "dolphin"
    }, {
    "abbr": "Dor",
    "name": "Dorado",
    "genitive": "Doradus",
    "en": "dolphinfish"
    }, {
    "abbr": "Dra",
    "name": "Draco",
    "genitive": "Draconis",
    "en": "dragon"
    }, {
    "abbr": "Equ",
    "name": "Equuleus",
    "genitive": "Equulei",
    "en": "pony"
    }, {
    "abbr": "Eri",
    "name": "Eridanus",
    "genitive": "Eridani",
    "en": "river Eridanus (mythology)"
    }, {
    "abbr": "For",
    "name": "Fornax",
    "genitive": "Fornacis",
    "en": "chemical furnace"
    }, {
    "abbr": "Gem",
    "name": "Gemini",
    "genitive": "Geminorum",
    "en": "twins"
    }, {
    "abbr": "Gru",
    "name": "Grus",
    "genitive": "Gruis",
    "en": "Crane"
    }, {
    "abbr": "Her",
    "name": "Hercules",
    "genitive": "Herculis",
    "en": "Hercules (mythological character)"
    }, {
    "abbr": "Hor",
    "name": "Horologium",
    "genitive": "Horologii",
    "en": "pendulum clock"
    }, {
    "abbr": "Hya",
    "name": "Hydra",
    "genitive": "Hydrae",
    "en": "Hydra (mythological creature)"
    }, {
    "abbr": "Hyi",
    "name": "Hydrus",
    "genitive": "Hydri",
    "en": "lesser water snake"
    }, {
    "abbr": "Ind",
    "name": "Indus",
    "genitive": "Indi",
    "en": "Indian"
    }, {
    "abbr": "Lac",
    "name": "Lacerta",
    "genitive": "Lacertae",
    "en": "lizard"
    }, {
    "abbr": "Leo",
    "name": "Leo",
    "genitive": "Leonis",
    "en": "lion"
    }, {
    "abbr": "LMi",
    "name": "Leo Minor",
    "genitive": "Leonis Minoris",
    "en": "lesser lion"
    }, {
    "abbr": "Lep",
    "name": "Lepus",
    "genitive": "Leporis",
    "en": "hare"
    }, {
    "abbr": "Lib",
    "name": "Libra",
    "genitive": "Librae",
    "en": "balance"
    }, {
    "abbr": "Lup",
    "name": "Lupus",
    "genitive": "Lupi",
    "en": "wolf"
    }, {
    "abbr": "Lyn",
    "name": "Lynx",
    "genitive": "Lyncis",
    "en": "lynx"
    }, {
    "abbr": "Lyr",
    "name": "Lyra",
    "genitive": "Lyrae",
    "en": "lyre / harp"
    }, {
    "abbr": "Men",
    "name": "Mensa",
    "genitive": "Mensae",
    "en": "Table Mountain (South Africa)"
    }, {
    "abbr": "Mic",
    "name": "Microscopium",
    "genitive": "Microscopii",
    "en": "microscope"
    }, {
    "abbr": "Mon",
    "name": "Monoceros",
    "genitive": "Monocerotis",
    "en": "unicorn"
    }, {
    "abbr": "Mus",
    "name": "Musca",
    "genitive": "Muscae",
    "en": "fly"
    }, {
    "abbr": "Nor",
    "name": "Norma",
    "genitive": "Normae",
    "en": "carpenter's level"
    }, {
    "abbr": "Oct",
    "name": "Octans",
    "genitive": "Octantis",
    "en": "octant (instrument)"
    }, {
    "abbr": "Oph",
    "name": "Ophiuchus",
    "genitive": "Ophiuchi",
    "en": "serpent-bearer"
    }, {
    "abbr": "Ori",
    "name": "Orion",
    "genitive": "Orionis",
    "en": "Orion (mythological character)"
    }, {
    "abbr": "Pav",
    "name": "Pavo",
    "genitive": "Pavonis",
    "en": "peacock"
    }, {
    "abbr": "Peg",
    "name": "Pegasus",
    "genitive": "Pegasi",
    "en": "Pegasus (mythological creature)"
    }, {
    "abbr": "Per",
    "name": "Perseus",
    "genitive": "Persei",
    "en": "Perseus (mythological character)"
    }, {
    "abbr": "Phe",
    "name": "Phoenix",
    "genitive": "Phoenicis",
    "en": "phoenix"
    }, {
    "abbr": "Pic",
    "name": "Pictor",
    "genitive": "Pictoris",
    "en": "easel"
    }, {
    "abbr": "Psc",
    "name": "Pisces",
    "genitive": "Piscium",
    "en": "fishes"
    }, {
    "abbr": "PsA",
    "name": "Piscis Austrinus",
    "genitive": "Piscis Austrini",
    "en": "southern fish"
    }, {
    "abbr": "Pup",
    "name": "Puppis",
    "genitive": "Puppis",
    "en": "poop deck"
    }, {
    "abbr": "Pyx",
    "name": "Pyxis",
    "genitive": "Pyxidis",
    "en": "mariner's compass"
    }, {
    "abbr": "Ret",
    "name": "Reticulum",
    "genitive": "Reticuli",
    "en": "eyepiece graticule"
    }, {
    "abbr": "Sge",
    "name": "Sagitta",
    "genitive": "Sagittae",
    "en": "arrow"
    }, {
    "abbr": "Sgr",
    "name": "Sagittarius",
    "genitive": "Sagittarii",
    "en": "archer"
    }, {
    "abbr": "Sco",
    "name": "Scorpius",
    "genitive": "Scorpii",
    "en": "scorpion"
    }, {
    "abbr": "Scl",
    "name": "Sculptor",
    "genitive": "Sculptoris",
    "en": "sculptor"
    }, {
    "abbr": "Sct",
    "name": "Scutum",
    "genitive": "Scuti",
    "en": "shield (of Sobieski)"
    }, {
    "abbr": "Ser",
    "name": "Serpens",
    "genitive": "Serpentis",
    "en": "snake"
    }, {
    "abbr": "Sex",
    "name": "Sextans",
    "genitive": "Sextantis",
    "en": "sextant"
    }, {
    "abbr": "Tau",
    "name": "Taurus",
    "genitive": "Tauri",
    "en": "bull"
    }, {
    "abbr": "Tel",
    "name": "Telescopium",
    "genitive": "Telescopii",
    "en": "telescope"
    }, {
    "abbr": "Tri",
    "name": "Triangulum",
    "genitive": "Trianguli",
    "en": "triangle"
    }, {
    "abbr": "TrA",
    "name": "Triangulum Australe",
    "genitive": "Trianguli Australis",
    "en": "southern triangle"
    }, {
    "abbr": "Tuc",
    "name": "Tucana",
    "genitive": "Tucanae",
    "en": "toucan"
    }, {
    "abbr": "UMa",
    "name": "Ursa Major",
    "genitive": "Ursae Majoris",
    "en": "great bear"
    }, {
    "abbr": "UMi",
    "name": "Ursa Minor",
    "genitive": "Ursae Minoris",
    "en": "lesser bear"
    }, {
    "abbr": "Vel",
    "name": "Vela",
    "genitive": "Velorum",
    "en": "sails"
    }, {
    "abbr": "Vir",
    "name": "Virgo",
    "genitive": "Virginis",
    "en": "virgin or maiden"
    }, {
    "abbr": "Vol",
    "name": "Volans",
    "genitive": "Volantis",
    "en": "flying fish"
    }, {
    "abbr": "Vul",
    "name": "Vulpecula",
    "genitive": "Vulpeculae",
    "en": "fox"
    }]

    constellations_titlecase = constellation.title()
    for i in range(0, len(constellations)):
        if constellations[i]["name"] == constellations_titlecase:
            embed = discord.Embed(title = "Constellation chart", colour = 0x1b30b3)
            embed.add_field(name = "IAU abbreviation", value = constellations[i]["abbr"], inline = False)
            embed.add_field(name = "IAU name", value =  constellations[i]["name"], inline = False)
            embed.add_field(name = "Genetive name", value = constellations[i]["genitive"], inline = False)
            embed.add_field(name = "Depicture/character", value = constellations[i]["en"], inline = False)
            await ctx.send(embed = embed)

@bot.command(aliases = ["m", "M"])
@commands.cooldown(rate = 1, per = 10, type = commands.BucketType.user)
async def messier(ctx, messierID):
    #Insert JSON here 
    await ctx.send("Command will be available soon!")



bot.run(os.getenv("token"))
