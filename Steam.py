import requests
import telegram

appid = input("Input the appid: ")

api = "https://store.steampowered.com/api/appdetails/?appids=" + appid

r = requests.get(api)
data = r.json()

try:
    discount_percent = data[appid]["data"]["price_overview"]["discount_percent"]

except TypeError:
    print("Invalid Input")
    quit()
except KeyError:
    print("Invalid appid")
    quit()
except KeyboardInterrupt:
    print("Exiting out")
    quit()
except NameError:
    print("NameError")
    quit()

price = data[appid]["data"]["price_overview"]["final_formatted"]

def notify_ending(message):
        chat_id = "telegram_chat_id"
        token = "telegram_token"
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id, text=message)


if discount_percent == 0:
    print("No discount \nPrice: " + price)
elif discount_percent > 0:
    print("Discount!! \nNew Price: " + price)
    notify_ending("New Discount for " + appid +  "\nNew Price = " + price)
