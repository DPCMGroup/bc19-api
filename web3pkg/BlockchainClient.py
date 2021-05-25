from web3 import Web3, HTTPProvider
from threading import Thread
import time
import hashlib
import traceback


class Client:

    def __init__(self, blockchain_address="http://127.0.0.1:8545"):
        '''
        Costruisce un client per la comunicazione con la blockchain
        :param str blockchain_address: l'indirizzo, solitamente url, della blockchain
        '''
        self.web3 = Web3(HTTPProvider(blockchain_address))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        # il tread che si sta utilizzando per ascoltare la blockchain, se esistente, altrimento None
        self.listeningThread = None
        # quando running è false e il thread lo legge, esso si ferma
        self.running = False

    def sendTransaction(self, byteData):
        '''
        Invia una transazione dall'account di default all'account di default.
        Inserisce nella transazione i dati passati in byteData, che devono essere appunto byte.

        :param str byteData: la stringa da inviare come contenuto della transazione

        Resituisce l'hash della transazione inviata.
        '''

        # byteData = bytes(dataString, 'utf-8');

        tx_hash = self.web3.eth.send_transaction(
            {'to': self.web3.eth.defaultAccount, 'from': self.web3.eth.defaultAccount, 'data': byteData});
        return tx_hash

    def hashAndSendData(self, dataString):
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
            return self.hashAndSendData(text)



    # return sendTransaction( f"\{ \"azione\": \"imposta stato postazione\", \"id postazione\": \"{id}\", \"stato\": \"{state}\"\}" )

    def log_loop(self, transaction_hash, poll_interval, callback_function, failure_callback_function):
        '''
        :param event_filter: il filtro usato per sleezionare solo alcune tra tutte le transazioni che verranno minate
        :param float poll_interval: l'intervallo tra le ispezioni eseguite sulla blockchain per trovare nuove transazioni minate
        :param callback_function: la funziona che verrà chiamata quando verrà rilevata una transazione eseguita
        '''
        found = False
        maxFailures = 3
        count = 0
        while self.running and not found and not count >= maxFailures:
            try:
                if (not count == 0):
                    time.sleep(poll_interval)
                receipt = self.web3.eth.getTransactionReceipt(transaction_hash)
                found = True
                print("transaction found")
                tx = self.web3.eth.get_transaction(transaction_hash)
                # print(trans)
                callback_function(receipt, tx)
            except:
                # traceback.print_exc()
                print("transaction not found")
                count += 1

        if (count >= maxFailures):
            failure_callback_function()

        print("end of thread")
        self.running = False

    def startListening(self, transaction_hash, callback_function, failure_callback_function):
        '''
        :param transaction_hash: l'hash della transazione per la quale aspettare il minaggio. Deve essere in byte
        :param callback_function: la funziona che verrà chiamata quando verrà rilevata una transazione minata.
                                    Vi si può passare anche una funzione esterna a questa classe.
        '''
        # block_filter = self.web3.eth.filter('latest')
        # tx_filter = self.web3.eth.filter('pending')
        self.listeningThread = Thread(target=self.log_loop,
                                      args=(transaction_hash, 5, callback_function, failure_callback_function),
                                      daemon=True)  # daemon=True non so se sia la cosa giusta da usare
        self.running = True
        self.listeningThread.start()

        print("started listening")

    # per adesso non usare questa funzione
    def stopListening(self):
        self.running = False
        self.listeningThread.join()
        self.listeningThread = None
        print("stopped listening")

    def isAlive(self):
        return (not self.listeningThread == None) and self.listeningThread.isAlive()

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

    def bytesToString(self, bytes):
        return "0x" + "".join([hex(b)[2:] for b in bytearray(bytes)])





