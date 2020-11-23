import pymongo 
from pymongo import MongoClient 
import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw
import requests
import io
import asyncio

cluster = MongoClient("mongodb+srv://nexxon028:Loker456@cluster0-6whlk.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["user_list"]
client = discord.Client()
bot = commands.Bot(command_prefix="/")

TOKEN = 'NzEzNzM5OTc4NTk2Njc5NzEw.XukqtA.h43q0Y98Jun5y07hI-m7OMVdRdA'

COLORS = [discord.Color.red(), discord.Color.green(), discord.Color.blue()]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@bot.command()
async def калл(ctx, *args):
    answers = ['да', 'нет']
    await ctx.send(str(random.choice(answers)))


@bot.command()
async def start(ctx):
    words = ["кал", "не кал", 'Otcoci', 'GoW(но)', 'Быдло школоте не понять', 'Графика из скайрима 2011 года', 'Вот и все']
    if str(ctx.author.id) == '502121096271757333':
        while True:
            time = 900
            await asyncio.sleep(time)
            await ctx.send(random.choice(words))
    else:
        await ctx.send('Чё надо?')


@bot.command()
async def ставка(ctx, arg=None):

    global COLORS

    channels = ['casino']
    user_post = {"user_id": ctx.author.id, "balance": 10}
    result = collection.find_one({"user_id": ctx.author.id})
    if result is None:
        collection.insert_one(user_post)
   

    try:
        arg = int(arg)
    except:
        emb = discord.Embed(title="Ошибка", colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value=f"Бот принимает только целые числа!")
        await ctx.send(embed=emb)
        
    if isinstance(arg, float):
        emb = discord.Embed(title="Ошибка", colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value=f"Бот принимает только целые числа!")
        await ctx.send(embed=emb)

    elif arg is None:
        emb = discord.Embed(title="Ошибка", colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value=f"Укажите ставку!")
        await ctx.send(embed=emb)
        
    cof = random.randint(0, 5)
    win_cash = int(arg) * cof
    num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
    if str(arg) in num_list:
        emb = discord.Embed(title="Ошибка", colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Минимальная ставка 10 рублей')
        await ctx.send(embed=emb)

    elif int(float(arg)) <= int(result["balance"]) and str(arg) not in num_list:
        bet = int(arg)
        old_val = {"balance": result["balance"]}
        new_val = {"$set": {"balance": result["balance"] - bet + int(win_cash)}}
        collection.update_one(old_val, new_val)
        emb = discord.Embed(title="Ставка", colour=random.choice(COLORS))
        emb.add_field(name=ctx.author.name, value=f"Ставка {arg}\nМножитель: {win_cash/bet}x\nВыигрыш: {str(win_cash)}🤘")
        await ctx.send(embed=emb)

    if result["balance"] == 0:
        emb = discord.Embed(title="Ошибка", colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы бомж\nВведите /moneybonus для пополнения баланса')
        await ctx.send(embed=emb)

    


@bot.command()
async def баланс(ctx):
    user_post = {"user_id": ctx.author.id, "balance": 10}
    check = collection.find_one({"user_id": ctx.author.id})
    if check is None:
        collection.insert_one(user_post)
        check = collection.find_one(user_post)
        balance = check["balance"]
        emb = discord.Embed(title="Баланс", colour=discord.Color.blue())
        emb.add_field(name=ctx.author.name, value=f"Ваш баланс: {balance} рублей")
        await ctx.send(embed=emb)
    else:
        balance = check["balance"]
        emb = discord.Embed(title="Баланс", colour=discord.Color.blue())
        emb.add_field(name=ctx.author.name, value=f"Ваш баланс: {balance} рублей")
        await ctx.send(embed=emb)

@bot.command()
async def moneybonus(ctx):
    bonus = 10
    user_post = {"user_id": ctx.author.id, "balance": 10}
    result = collection.find_one({"user_id": ctx.author.id})
    if result is None:
        collection.insert_one(user_post)
        emb = discord.Embed(title="Бонус", colour=discord.Color.green())
        emb.add_field(name=ctx.author.name, value=f"Ваш баланс пополнен на 10 рублей")
        await ctx.send(embed=emb)
    else:
        old_val = {"balance": result["balance"]}
        new_val = {"$set": {"balance": result["balance"] + bonus}}
        collection.update_one(old_val, new_val)
        emb = discord.Embed(title="Бонус", colour=discord.Color.green())
        emb.add_field(name=ctx.author.name, value=f"Ваш баланс пополнен на 10 рублей")
        await ctx.send(embed=emb)


#@bot.command()
#async def профіль(ctx):
#    img = Image.new("RGBA", (350, 140), '#3b3b3b')
#    url = str(ctx.author.avatar_url)[:-10]
#    response = requests.get(url, stream=True)
#    r = Image.open(io.BytesIO(response.content))
#    r = r.convert('RGBA')
 #   r = r.resize((100, 100), Image.ANTIALIAS)
#
#    img.paste(r, (15, 15, 115, 115))
#
#    draw = ImageDraw.Draw(img)
#    name = ctx.author.name
#    tag = ctx.author.discriminator #tag example: #9830
#    
#    head_line = ImageFont.truetype('arial.ttf', size=20)
#    under_text = ImageFont.truetype('arial.ttf', size=15)
#    balans = ImageFont.truetype('arial.ttf', size=15)
#
#    user_post = {"user_id": ctx.author.id, "balance": 10}
 #   result = collection.find_one({"user_id": ctx.author.id})
#    if result is None:
#        collection.insert_one(user_post)
#        result = collection.find_one({"user_id": ctx.author.id})
#        money = str(result["balance"])
#        draw.text((120, 15), f"{name}#{tag}", font=head_line)
#        draw.text((120, 50), f"ID: {ctx.author.id}", font=under_text)
#        draw.text((120, 75), f"Гроші: {money}", font=balans)
#
#        img.save('user_card.png')
#        await ctx.send(file=discord.File(fp=r'user_card.png'))
#    else:
#        result = collection.find_one({"user_id": ctx.author.id})
#        money = str(result["balance"])
#        draw.text((120, 15), f"{name}#{tag}", font=head_line)
#        draw.text((120, 50), f"ID: {ctx.author.id}", font=under_text)
#        draw.text((120, 75), f"Гроші: {money}", font=balans)
#
#        img.save('user_card.png')
#        await ctx.send(file=discord.File(fp=r'D:\Python\my_projects\Discord\Photos\user_card.png'))

bot.run(TOKEN)
