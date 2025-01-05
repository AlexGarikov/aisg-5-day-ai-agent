import telebot
from telebot import types
import PIL
import os
from dotenv import load_dotenv
from ai_agent import AI_Agent


print('Start creating the telegram bot')
# create the bot instance

# Load environment variables from .env file
load_dotenv()
CHAT_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
GEMINI_API_KEY = os.getenv("SECRET_KEY")

ai_agent = AI_Agent(gemini_api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(CHAT_BOT_KEY)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Add two buttons
    #markup = get_bot_buttons()

    # This is an option step, here it is just for example
    onboarding_image = PIL.Image.open('onboarding_image.jpg')

    bot.send_photo(m.chat.id, onboarding_image)
    msg = "Welcome to our agentic AI dentist appointments bot!"
    msg += "\n\nI can make an appointment for you to the doctor. Just ask me for an available time slot. Also I can cancel or move your current appointment"
    bot.send_message(m.chat.id, msg, reply_markup=None)

# The function to process an user request
@bot.message_handler(content_types=["text"])
def handle_text(msg):
    user_input = msg.text.strip().lower()

    # CHANGE THE process_user_request
    user_info = f'user name: "{msg.from_user.first_name} {msg.from_user.last_name}" user_id: {msg.from_user.id}'
    answer = process_user_request(f'({user_info}) {user_input}')
    #answer = message.from_user

    bot.send_message(msg.chat.id, answer, parse_mode='HTML')

def process_user_request(user_input):
    # USE A LLM to parse the text and prepare an answer
    result_msg = ai_agent.do_action(user_input)
    return result_msg


# Handles all sent documents and audio files
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    pass
#    try:
#        handle_photos_processor(message)
#    except:
#        tb = traceback.format_exc()
#        tb = get_user_info_from_msg(message) + '\n' + save_user_photos(message, ERROR_USERS_IMAGES_FOLER) + '\n' + tb
#        log_exeption(tb)
#        bot.send_message(message.chat.id, 'An error has happened')


print("bot is ready")
# Run the bot
bot.polling(none_stop=True, interval=0)
print("bot is finished")
