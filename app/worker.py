import time
import db
import models
from pyrogram.types import ReplyKeyboardMarkup as Markup
from pyrogram import Client, filters

bot = Client('mahdi')

def check_status(req_id):
    """
    Checks the status of a request using its req_id.
    Returns the status of the request.
    """
    model_id = "clarity-upscaler"  # Example model_id; adjust based on your actual use
    status = models.get_status(model_id, req_id)
    return status

def process_completed_request(req_id, user_id):
    """
    Processes a request that has been completed.
    Update user and request status in the database.
    """
    # Retrieve the request result
    model_id = "clarity-upscaler"  # Example model_id; adjust based on your actual use
    result = models.get_result(model_id, req_id)

    # Handle the result (e.g., notify the user, update the database)
    print(f"Request {req_id} completed. Result: {result}")

    # Update the request status in the database
    db.update_request(req_id, 'completed', True)
    
    # Notify the user or update user record as needed
    bot.send_message(user_id, f'your request is done\n{result}')
    # Example: You can use a notification system or send messages through Telegram API

def main():
    while True:
        # Fetch all requests that are not completed
        requests = db.get_all_requests()  # Implement this function in db.py

        for request in requests:
            req_id = request[1]
            user_id = request[3]
            status = check_status(req_id)

            if status['status'] == 'COMPLETED':  # Adjust based on the actual status response
                process_completed_request(req_id, user_id)

        # Sleep for a while before checking again (e.g., 5 minutes)
        time.sleep(300)

if __name__ == "__main__":
    main()
