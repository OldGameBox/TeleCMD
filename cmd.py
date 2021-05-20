import telebot
import subprocess
import os
import atexit
import datetime

mode=2
users = []
def load_users():
    file = open("users.cfg","r")
    for line in file.readlines():
        users.append(line[0:len(line)-1])
    print(users)
    file.close()

load_users()
bot = telebot.TeleBot("")
time = datetime.datetime.now()
log=""

def exit_handler():
    file_name = "telecmd_log_"+str(time.day)+":"+str(time.month)+":"+str(time.year)+"-"+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+".log"
    file = open(file_name,"w+")
    file.write(log)
    file.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        bot.reply_to(message, "Welcome admin!")
    else:
        bot.reply_to(message, "Sorry you aren't able to control this mainframe.")

@bot.message_handler(commands=['logs'])
def send_logs(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        bot.reply_to(message, log)
    else:
        bot.reply_to(message, "Sorry you aren't able to control this mainframe.")

@bot.message_handler(commands=['savelogs'])
def save_logs(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        exit_handler()
    else:
        bot.reply_to(message, "Sorry you aren't able to control this mainframe.")
    
@bot.message_handler(commands=['getaccess'])
def getaccess(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        bot.reply_to(message, "You already able to control this mainframe.")
    else:
        bot.reply_to(message, "Contact with Boss:\nhttps://discord.gg/SwA9mG9bAh \nor\noldgamebox.micheal@gmail.com")

@bot.message_handler(commands=['stop'])
def stop(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        bot.reply_to(message, "Service stopped. Reboot server to start service again.")
        save_logs(message)
        exit()
    else:
        bot.reply_to(message, "Sorry, you aren't able to control this mainframe.")

@bot.message_handler(commands=['users'])
def send_users(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        bot.reply_to(message, str(users))
    else:
        bot.reply_to(message, "Sorry, you aren't able to control this mainframe.")

@bot.message_handler(commands=['adduser'])
def add_user(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        if len(message.text) > 9:
            users.append(message.text[9:len(message.text)])
            save_users()
            bot.reply_to(message, "User added: "+message.text[9:len(message.text)])
        else:
            bot.reply_to(message, "Use this command like this: /adduser [username]")
    else:
        bot.reply_to(message, "Sorry, you aren't able to control this mainframe.")

@bot.message_handler(commands=['removeuser'])
def remove_user(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
    if message.from_user.username in users:
        if len(message.text) > 9:
            try:
                users.remove(message.text[9:len(message.text)])
                save_users()
                bot.reply_to(message, "User removed: "+message.text[9:len(message.text)])
            except:
                bot.reply_to(message, message.text[9:len(message.text)]+" is not in users")
        else:
            bot.reply_to(message, "Use this command like this: /removeuser [username]")
    else:
        bot.reply_to(message, "Sorry, you aren't able to control this mainframe.")

def save_users():
    file = open("users.cfg","w+")
    for user in users:
        file.write(user+"\n")
    file.close()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global log
    print(message.from_user.username)
    print(message.text)
    log += message.from_user.username + "\n"
    log += message.text + "\n"
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
            print(out)
            if not isinstance(out, str):
                out = out.decode('latin-1')
            bot.reply_to(message, "Resualt:"+out)
            log += out + "\n"
        except:
            bot.reply_to(message, "Resualt: Error | "+message.text)
            log += "Error\n"
    else:
        bot.reply_to(message, "Sorry, you aren't able to control this mainframe.")

bot.polling()

atexit.register(exit_handler)
