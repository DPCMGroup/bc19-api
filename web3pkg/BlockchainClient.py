from web3 import Web3, HTTPProvider
from AdminApp.cron import txCompleteHandle, fail
import time
from datetime import datetime
import hashlib


class Client:

    def __init__(self, blockchain_address="http://dpcm2077.duckdns.org:8545"):
        '''
        Costruisce un client per la comunicazione con la blockchain
        :param str blockchain_address: l'indirizzo, solitamente url, della blockchain
        '''
        self.web3 = Web3(HTTPProvider(blockchain_address))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        # il tread che si sta utilizzando per ascoltare la blockchain, se esistente, altrimento None

    def sendTransaction(self, stringData):
        '''
        Invia una transazione dall'account di default all'account di default.
        Inserisce nella transazione i dati passati in byteData, che devono essere appunto byte.

        :param str byteData: la stringa da inviare come contenuto della transazione

        Resituisce l'hash della transazione inviata.
        '''

        # byteData = bytes(dataString, 'utf-8')

        tx_hash = self.web3.eth.send_transaction(
            {'to': self.web3.eth.defaultAccount, 'from': self.web3.eth.defaultAccount, 'data': stringData})
        return tx_hash

    def hashAndSendByteData(self, data):
        hsh = self.hashByteData(data)
        return self.sendTransaction(hsh)

    def hashAndSendStringData(self, dataString):
        '''
        Prende la stringa di input, ne ottiene l'hash e lo invia alla blockchain
        Richiede una stringa (non byte)
        '''
        hsh = self.hashString(dataString)
        return self.sendTransaction(hsh)

    def hashAndSendFile(self, filePath):
        '''
        Legge il file di input in una string, ne ottiene l'hash e lo invia alla blockchain
        Richiede una stringa rappresentante il percorso di un file
        '''
        with open(filePath, "r") as file:
            text = file.read()
            return self.hashAndSendStringData(text)

    def log_loop(self, transaction_hash, poll_interval, limit=None):
        '''
        :param float poll_interval: l'intervallo tra le ispezioni eseguite sulla blockchain per trovare nuove transazioni minate
        :param callback_function: la funziona che verrà chiamata quando verrà rilevata una transazione eseguita
        '''
        found = False
        count = 0
        maxFailures = limit if limit != None else 1
        while not found and not count >= maxFailures:
            try:
                receipt = self.web3.eth.getTransactionReceipt(transaction_hash)
                found = True
                print(datetime.now().strftime("%Y-%m-%d %H:%M") + " transaction found", flush=True)
                tx = self.web3.eth.get_transaction(transaction_hash)
                data = tx.input
                # print(trans)
                txCompleteHandle(self.bytesToString(transaction_hash), data)
            except Exception as e:
                # traceback.print_exc()
                print(datetime.now().strftime("%Y-%m-%d %H:%M") + " transaction not found", flush=True)
                if (limit != None):
                    count += 1
            time.sleep(poll_interval)

        if (count >= maxFailures):
            fail()

        print(datetime.now().strftime("%Y-%m-%d %H:%M") + " end of tx_loop", flush=True)

    def startListening(self, transaction_hash, limit=None):
        '''
        :param transaction_hash: l'hash della transazione per la quale aspettare il minaggio. Deve essere in byte
        :param callback_function: la funziona che verrà chiamata quando verrà rilevata una transazione minata.
                                    Vi si può passare anche una funzione esterna a questa classe.
        '''
        # block_filter = self.web3.eth.filter('latest')
        # tx_filter = self.web3.eth.filter('pending')
        print(datetime.now().strftime("%Y-%m-%d %H:%M") + " started listening", flush=True)
        self.log_loop(transaction_hash, 10, limit)

    def hashString(self, string):
        '''
        Resituisce l'hash di string in byte.
        Richiede una stringa (non byte)
        '''
        byteData = bytes(string, 'utf-8')
        m = hashlib.sha256()
        m.update(byteData)
        digest = m.digest()
        # print(digest)
        hexString = self.bytesToString(digest)
        return hexString

    def hashByteData(self, data):
        '''
        Resituisce l'hash dei byte passati.
        Richiede byte in input
        '''
        m = hashlib.sha256()
        m.update(data)
        digest = m.digest()
        hexString = self.bytesToString(digest)
        return hexString

    def bytesToString(self, bytes):
        return "0x" + "".join([hex(b)[2:] for b in bytearray(bytes)])

    def getHashFromReceipt(rec):
        return rec['input']
