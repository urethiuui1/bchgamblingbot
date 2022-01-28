from app import database
from app import gamble
from bitcash import Key, PrivateKey
import bitcash
import telegram
from time import sleep
import hashlib
import logging
from datetime import datetime
from app import payouts
bchaddress = "" # BCH address of your hot wallet
tgtoken = "" # Telegram bot token

def sweep_all(k, destaddress):
            m = hashlib.sha256()
            if int(k.get_balance()) > 0:
                    fee = bitcash.network.get_fee(speed='slow')
                    outp = []
                    done = False
                    balance = k.get_balance()
                    outp.append((destaddress, balance, "satoshi"))
                    while(not(done)):
                        if int(balance) < 0:
                            return -1
                        try:
                            k.send(outp, fee=1, combine=True)
                            done = True
                        except Exception as e:
                            outp = []
                            fee = fee + 1
                            outp.append((destaddress, int(balance)-fee, "satoshi"))
                    return (int(balance)-fee)
            else:
                return -1        


def main():
    logging.basicConfig(filename="pastgames.log",
                                filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%H:%M:%S',
                                level=logging.INFO)



    DB = database.Database_cl()
    Gamble = gamble.Gamble_cl()
    bot = telegram.Bot(token=tgtoken)
    POqueue = payouts.Database_cl()

    while(1):
        jackpot = 100000
        txs = DB.getDB()
        for tx in txs:
            txid = ""
            pK = tx[1]
            pubK = tx[2]
            retAdr = tx[3]
            chatid = tx[4]
            seed = tx[5]
            won = tx[6]
            timestp = tx[7]
            K = Key(pK)
            bolenzA = K.get_balance()
            DB.deleteTimeout()

            if int(bolenzA) > 0:
                    logging.info(pK + ":" + retAdr + ":" + seed)
                    if(int(bolenzA) > 400000 or int(bolenzA) < 5000):
                        sweep_all(K, bchaddress)
                        bot.send_message(chat_id=int(chatid), text="Thank you for your donation!")
                        DB.deleteEntry(tx[0])

                    txid = K.get_transactions()[0]
                    gseed = seed + str(int(txid, 16))
                    G = gamble.Gamble_cl()
                    G.setSeed(gseed)
                    won = G.gamble()
                    bolenz = 0
                    bolenz = (int(K.get_balance()) *2)
                    if (int(won) == 1 and bolenz > 0) or (int(won) == 777 and bolenz > 0):
                        if sweep_all(K, bchaddress) > 0:
                            if int(won) == 777:
                                bot.send_message(chat_id=int(chatid), text="You won the Jackpot!\nAdditional " + str(jackpot) + " BCH are sent to your wallet!" )
                                POqueue.insertEntry(tx[0]+str(777), retAdr, jackpot)
                                POqueue.insertEntry(tx[0], retAdr, bolenz)
                                DB.deleteEntry(tx[0])
                                bot.send_message(chat_id=int(chatid), text="You have won " + str(int(bolenz)/100000000) +" BCH!")
                                bot.send_message(chat_id=int(chatid), text="The plaintext seed is:\n\n" + str(seed) + str(int(txid, 16)))
                            elif int(won) == 1:
                                POqueue.insertEntry(tx[0], retAdr, bolenz)
                                DB.deleteEntry(tx[0])
                                bot.send_message(chat_id=int(chatid), text="You have won " + str(int(bolenz)/100000000) +" BCH!")
                                bot.send_message(chat_id=int(chatid), text="The plaintext seed is:\n\n" + str(seed) + str(int(txid, 16)))                           
                        else:
                            pass
                    elif int(won) == 0:
                        if sweep_all(K, bchaddress) > 0:
                            DB.deleteEntry(tx[0])
                            bot.send_message(chat_id=int(chatid), text="You have lost " + str(int(bolenzA)/100000000) +" BCH!")
                            bot.send_message(chat_id=int(chatid), text="The plaintext seed is:\n\n" + str(seed) + str(int(txid, 16)))
                        else:
                            pass


        sleep(9)            

if __name__ == "__main__":
    main()    
