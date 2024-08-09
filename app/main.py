from pyrogram import Client, filters
from PIL import Image 
import os
from pyrogram.types import ReplyKeyboardMarkup as Markup
from models import upload, tryon, clarity_upscale
import requests
from io import BytesIO
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import db

# bot_api = '6752497249:AAE_1UP_pVxNd3vMsKXnIA6QEbvIGRplUfU'
# bot = Client('mahdi',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6')
inp_dir = 'inputs/'
os.makedirs(inp_dir)

out_dir = 'outputs/'
os.makedirs(out_dir)

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
        if(db.get_user(chat_id)[7] != 'COMPLETED'):
            if(os.path.exists(photo)):
                if(data == 'creative_upscale'):
                    await callback_query.answer("✅درخواست شما ثبت شد", show_alert = False)
                    await message.delete()

                    url = upload(photo)
                    db.update_user(chat_id, 'image_path', url)

                    req_id = clarity_upscale(url)
                    db.add_request(req_id, chat_id)
                    await message.reply("✅درخواست شما ثبت شد\nلطفا کمی منتظر باشید.")
                    
            else:
                await client.send_message(chat_id, 'لطفا اول یک عکس آپلود کنید')
        else : 
            await message.reply('شما یک درخواست در حال انجام دارید، تا پایان درخواست قبلی، نمی‌توانید درخواست جدیدی ثبت کنید.\nلطفا کمی منتظر باشید🙏')
    else:
        await message.reply('شما هنوز در این ربات ثبت نام نکرده اید. از این دستور برای شروع ربات استفاده کنید /start')


@bot.on_message(filters.private & filters.regex('/edit'))
async def edit_image(client, message):
    #edit both files
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'

    if(os.path.exists(person_img)):
        os.remove(person_img)
    if(os.path.exists(garment_img)):
        os.remove(garment_img)

    await message.reply('Ok, Please me a photo of the person you want to try on it.')

@bot.on_message(filters.private & filters.regex('/imagine_'))
async def imagine(client, message):

    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'
    description = ''
    garment_type = ''#upper_body lower_body dress

    if(message.text.startswith('/imagine_upper')): 
        garment_type = 'upper_body'
        description = message.text.replace('/imagine_upper', '')

    elif(message.text.startswith('/imagine_lower')): 
        garment_type = 'lower_body'
        description = message.text.replace('/imagine_lower', '')

    elif(message.text.startswith('/imagine_dress')): 
        garment_type = 'dress'
        description = message.text.replace('/imagine_dress', '')

    if(os.path.exists(person_img) and os.path.exists(garment_img)):
        if(description and garment_type):
            #generate image
            person_url = upload(person_img)
            garment_url = upload(garment_img)
            # await message.reply(person_url)
            # await message.reply(garment_url)
            await message.reply(f'Generating your image**{description}**, it can take up to 1 min, Please wait')

            img, msk = tryon(person_url, garment_url, description, garment_type)
            downloaded_path = download_image(img, chat_id)
            await client.send_photo(chat_id, downloaded_path, caption='You generated image')

            resized = resize_image(person_img ,downloaded_path)
            await client.send_photo(chat_id, resized, caption='your resized image')

            # await message.reply(img)
            # await message.reply(msk)

        else:
            await message.reply('You should send description for the garment with this format : /imagine_upper black shirt')
    else:
        await message.reply('You should submit both person and garment images, Use /images to check ')
    
@bot.on_message(filters.private & filters.regex('/images'))
async def images(client, message):
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'

    if(os.path.exists(person_img)):
        await client.send_photo(chat_id, person_img, caption='your person image')
    if(os.path.exists(garment_img)):
        await client.send_photo(chat_id, garment_img, caption='your garment image')
    if(not os.path.exists(person_img) and not os.path.exists(garment_img)):
        await message.reply('No images has been submitted, Send person image.')


@bot.on_message(filters.private & filters.regex('/save'))
async def save(client, message):
    chat_id = message.chat.id
    url = message.text.split(' ')[1]

    downloaded_path = download_image(url, chat_id)
    await client.send_photo(chat_id, downloaded_path, caption='your image')

@bot.on_message(filters.private & filters.regex('/resize'))
async def resize(client, message):
    chat_id = message.chat.id
    person_img = f'{root}{chat_id}/person.jpg'
    garment_img = f'{root}{chat_id}/garment.jpg'
    target = 'outputs/791927771-1.jpg'

    resized = resize_image(person_img, target)
    await client.send_photo(chat_id, resized, caption='resized image')

def download_image(url, id):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    count = len(os.listdir('outputs/')) + 1
    filename = f"outputs/{id}-{count}.jpg"

    image.save(filename)
    print(f'Image successfully downloaded and saved as {filename}')

    return filename

def resize_image(target, source):
    # Open the target image and the source image
    target_image = Image.open(target)
    source_image = Image.open(source)

    # Get the size of the target image
    target_size = target_image.size

    # Resize the source image to match the size of the target image
    resized_source_image = source_image.resize(target_size)

    # Save the resized image (optional)
    resized_source_image.save(source)

    # Display the resized image (optional)
    resized_source_image.show()

    return(source)
bot.run()