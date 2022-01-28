from app import payouts
from bitcash import Key
import logging
from time import sleep

hotwallet = "" # Private Key of your hot wallet

def main():
    logging.basicConfig(filename="payouts.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    payoutlist = payouts.Database_cl()

    while(1):
        lst = payoutlist.getDB()
        Wallet = Key(hotwallet)
        for i in lst:
            adr = i[1]
            sats = i[2]
            outp = [(adr, sats, "satoshi")]
            Wallet.get_balance()
            try:
                Wallet.send(outp, fee=1, combine=True)
                payoutlist.deleteEntry(i[0])
                logging.info(adr + ":" + sats + ":OK")
            except:
                logging.info(adr + ":" + sats + ":FAILED")
                sleep(2)


if __name__ == "__main__":
    main()
