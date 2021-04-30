import telebot
import subprocess
import os

mode=2
users = ["MRKUM2605", "softyjet"]
bot = telebot.TeleBot("1725300170:AAEXUPHxg8G-C4598d03SwwmPvPf9bA9HyY")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message.from_user.username)
    print(message.text)
    if message.from_user.username in users:
	    bot.reply_to(message, "Welcome admin!")
    else:
        bot.reply_to(message, "Sorry you aren't able to control this mainframe")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global mode
    if message.from_user.username in users:
        try:
            if message.text[0:3] == "cd ":
                path = message.text [3:len(message.text)]
                number  = os.chdir(path)
                out="Changed currect directory to "+path
            # elif message.text[1:2] == ":":
            #     path = message.text [0:2]
            #     number  = os.chdir(path)
            #     out="Changed currect drive to "+path+":"
            # elif message.text[0:5] == "mode 1":
            #     mode=1
            # elif message.text[0:5] == "mode 2":
            #     mode=2
            else:
                if mode==1:
                    out = subprocess.Popen(message.text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd() ).communicate()[0]
                if mode==2:
                    out = os.popen(message.text).read()
            print(message.from_user.username)
            print(message.text)
            print(out)
            if not isinstance(out, str):
                out = out.decode('latin-1')
            bot.reply_to(message, "Resualt:"+out)
        except:
            print(message.from_user.username)
            print(message.text)
            bot.reply_to(message, "Resualt: Error | "+message.text)
    else:
        print(message.from_user.username)
        print(message.text)
        bot.reply_to(message, "Sorry you aren't able to control this mainframe")

bot.polling()