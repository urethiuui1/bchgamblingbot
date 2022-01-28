from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
from app import payment
import re
tgtoken = "" # Telegram bot token
a = payment.Payment_cl()

def start(update, context):
    t = """
Welcome to my provable fair BCH gambling bot. ^^
You can double your BCH by a chance of 48%.
The currerent jackpot is 0.001 BCH!

    >> instant (~10 seconds), onchain, provable fair <<
        
Send your BCH address to this chat to start gambling!

WARNING: For every gamble you have to generate a new game by sending your BCH address to the chat!
After you send BCH to the deposit-address within 10 minutes the address can't be used again!
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)
     
def payoutaddress(update, context):
    x=re.compile('^((bitcoincash:)?(q|p)[a-z0-9]{41})')
    y=re.compile('^([13][a-km-zA-HJ-NP-Z1-9]{25,34})')
    z=re.compile('^((BITCOINCASH:)?(Q|P)[A-Z0-9]{41})$')
    address = update.message.text
    if x.match(address) == None and y.match(address) == None and z.match(address) == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please sent a valid BCH address!")
    else:
        if (y.match(address) == None) and (address.split(":")[0] != "bitcoincash" and address.split(":")[0] != "BITCOINCASH"):
            address = "bitcoincash:" + address
        b = a.generatePaymentInfo(address, update.effective_chat.id)

        context.bot.send_message(chat_id=update.effective_chat.id, text="The server seed is:\n\n" + str(b[2]))
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(address) + " \nis your payout address.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Send between 0.00005 and 0.004 BCH to the following >>ONETIME<<-address:")
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(b[1]))
        context.bot.send_message(chat_id=update.effective_chat.id, text="If your sent amount is not within the allowed range I interpret your deposit as a non-refundable donation!\n\nYou may only use the deposit address you get from the bot once!\n\nThis current game expires after 10 minutes!")
  
def info(update, context):
    t = """
The game generates a number between 0 and 1. random.random() - python3
If the random number is higher than 0.52, you win and get the double of your deposit back.
If the random number equals to 0.777 you win the jackpot.

Structure of the seed:
serverSeed + str(int(TXID, 16))
Bevore you send BCH you get a sha256 hashed server-seed.
After the game is played you recieve the whole seed in plaintext.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can use this python3 script to verify your game:\nhttps://pastebin.com/raw/afEcsuth")

def help(update, context):
    t = """
Step 1: Send your BCH address to the chat

Step 2: Send BCH to the deposit address you received from the bot

WARNING! You can only use the address for one transaction!
To play another round, you have to send your payout address again!
An unfunded game is cancelled after 10 minutes!

Step 3: Within ~10 seconds after your transaction you are notified if
you have won. If you win the BCH will be sent to you right away.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)




def main():


    updater = Updater(tgtoken, use_context=True)

    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('info', info)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('help', help)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), payoutaddress)
    dispatcher.add_handler(echo_handler)
    
    updater.start_polling()

if __name__ == '__main__':
    main()


