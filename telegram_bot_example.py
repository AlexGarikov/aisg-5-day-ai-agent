import telebot
from telebot import types
import PIL


print('Start creating the telegram bot')
# create the bot instance
CHAT_BOT_ID = '{A BOT ID}'

bot = telebot.TeleBot(CHAT_BOT_ID)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Add two buttons
    #markup = get_bot_buttons()

    # This is an option step, here it is just for example
    onboarding_image = PIL.Image.open('onboarding_image.jpg')

    bot.send_photo(m.chat.id, onboarding_image)
    msg = "Welcome to our dentist company appointments bot. I do for you: ....."
    bot.send_message(m.chat.id, msg, reply_markup=None)

# The function to process an user request
@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_input = message.text.strip().lower()

    # CHANGE THE process_user_request
    answer = process_user_request(user_input)

    bot.send_message(message.chat.id, answer, parse_mode='HTML')

def process_user_request(user_input):
    # USE A LLM to parse the text and prepare an answer
    pass


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
