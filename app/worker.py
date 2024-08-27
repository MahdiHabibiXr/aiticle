import schedule
import time
import db  
import models 
from pyrogram import Client, filters

# bot = Client('mahdi2',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6' )
bot = Client('mahdi2')

def check_and_update_tasks():
    # Get all jobs from the database
    tasks = db.get_all_jobs()
    
    for task in tasks:
        # Get the current status of the job
        user = task[1]
        job_type = task[2]
        user_image = task[4]
        print(f'Running {job_type} for {user}')

        try:
            result = models.clarity_upscale_run()
            with bot:
                bot.send_message(int(user), 'عکس شما با موفقیت ساخته شد، بفرمایید :')
                bot.send_photo(int(user), result, 'ساخته شده با عکسیفای')
                
            # bot.send_photo(int(user), user_image)

            print(f"Job {task[0]} done. Going to change it into the database")
            db.update_task(task[0], 'done', True)
            db.update_user(user, 'in_progress', False)

        except Exception as error:
            print(error)
            with bot:
                bot.send_message('791927771', error)

# Schedule the task to run every 5 minutes
schedule.every(5).minutes.do(check_and_update_tasks)

print("Job scheduler started. Checking jobs every 5 minutes...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
