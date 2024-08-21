from pyrogram import Client, filters
from PIL import Image 
import os
from pyrogram.types import ReplyKeyboardMarkup as Markup
from models import upload, clarity_upscale, credits
import requests
from io import BytesIO
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import db

# bot_api = '6752497249:AAE_1UP_pVxNd3vMsKXnIA6QEbvIGRplUfU'
# bot = Client('mahdi',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6')
inp_dir = 'inputs/'
# os.makedirs(inp_dir)

out_dir = 'outputs/'

root=''
bot = Client('mahdi')

links = ["@studAIo_styles", "@aiticle"]

async def is_joined(app , user_id):
    not_joined = []
    for channel in links:
        try:
            await app.get_chat_member(channel , user_id)
        except:
            not_joined.append(channel)
    return not_joined


@bot.on_message(filters.command("start"))
async def start_text(client, message):
    not_joined_channels = await is_joined(bot , message.from_user.id)
    t_id = message.chat.id

    #TODO: Check if its invited and add it to db

    #check if user exists
    if(not db.user_exists(t_id)):
        db.add_user(t_id)

    if not_joined_channels:
        await message.reply("🌹سلام دوست عزیز به این ربات خوش اومدی\n👈به کمک این ربات میتونی با هوش‌مصنوعی، عکسهات رو بازسازی کنی\n\nلطفا برای فعالسازی ربات، اول در این کانالها جوین شو و بعدش دوباره روی /start کلیک کن"
                            +'\n\n' + links[0] + '    ' + links[1])
    else:        
        await message.reply("😍تبریک میگم، حالا میتونی از قابلیت‌های ربات استفاده کنی، اول عکسی که میخوای به هوش‌مصنوعی بدی رو آپلود کن :")


@bot.on_message(filters.command('test') & filters.private)
async def test_bot(client, message):
    await message.reply('im upppp')


@bot.on_message(filters.private & filters.photo)
async def image(client, message):
    chat_id = message.chat.id
    input_img = f'{inp_dir}{chat_id}.jpg'
    
    file = await client.download_media(message.photo.file_id, file_name = f'{inp_dir}{chat_id}.jpg')

    #add file to db as latest image address
    caption = "🖼عکس ورودی شما ثبت شد، لطفا از دکمه‌های زیر یک گزینه رو انتخاب کنید :"
    markup = InlineKeyboardMarkup(
        [
            # [  # First row
            #     InlineKeyboardButton(  # Generates a callback query when pressed
            #         "🔄 افزایش کیفیت",
            #         callback_data="upscale"
            #     ),
            # ],
            [  # Second row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "🤖بازسازی با هوش‌مصنوعی",
                    callback_data="creative_upscale"
                ),
            ]
        ]
    )
    await client.send_photo(chat_id, file, reply_markup = markup, caption = caption)


@bot.on_callback_query()
async def callbacks(client, callback_query):
    message = callback_query.message
    data = callback_query.data
    chat_id = callback_query.from_user.id
    photo = f'{inp_dir}{chat_id}.jpg'

    if(db.user_exists(chat_id)):
        user_db = db.get_user(chat_id)
        if(user_db[6] == False): #TODO: check credits

            if(os.path.exists(photo)):
                if(data == 'creative_upscale'):
                    await callback_query.answer("✅درخواست شما ثبت شد", show_alert = False)
                    await message.delete()

                    url = upload(photo)
                    db.update_user(chat_id, 'image_path', url)
                    db.update_user(chat_id, 'in_progress', True)

                    db.add_job(chat_id, 'clarity')
                    await message.reply("✅درخواست شما ثبت شد\nلطفا کمی منتظر باشید.")
                    
            else:
                await client.send_message(chat_id, 'لطفا اول یک عکس آپلود کنید')
        else : 
            await message.reply('شما یک درخواست در حال انجام دارید، تا پایان درخواست قبلی، نمی‌توانید درخواست جدیدی ثبت کنید.\nلطفا کمی منتظر باشید🙏')
    else:
        await message.reply('شما هنوز در این ربات ثبت نام نکرده اید. از این دستور برای شروع ربات استفاده کنید /start')



@bot.on_message(filters.private & filters.regex('/credits'))
async def get_credits(client, message):
    key = message.text.replace('/credits', '')
    credit = credits(key)
    message.replace(credit)

bot.run()