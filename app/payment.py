from bitcash import Key, PrivateKey
from app import database
from app import gamble
import hashlib
from datetime import datetime
import logging
class Payment_cl(object):
    def __init__(self):
        self.DB = database.Database_cl()
        self.Gamble = gamble.Gamble_cl()
        logging.basicConfig(filename="allgames.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    def generatePaymentInfo(self, retaddress, chatid):
        key = Key()
        pid = hash(key.address + retaddress)
        seed = self.Gamble.createSeed()
        self.save(pid, key.to_wif(), key.address, retaddress, chatid, seed)
        m = hashlib.sha256()
        m.update((str(seed)).encode())
        hseed = m.hexdigest()

        logging.info("NEW GAME - " + key.to_wif() + ":" + retaddress + ":" + seed)


        return [pid, key.address, hseed]

    def save(self, pid, key, address, retaddress, chatid, seed):
        won = -1 
        T = datetime.now()
        self.DB.insertEntry(pid, key, address, retaddress, chatid, seed, won, str(T.now()).split(".")[0])

