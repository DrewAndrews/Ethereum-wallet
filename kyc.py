from web3 import Web3, HTTPProvider
from json import load
from sha3 import keccak_256
import requests
from time import sleep
from datetime import datetime
import sys


class AccountManager:
    def __init__(self):
        with open("network.json") as network:
            data = load(network)
            self.rpcUrl = data["rpcUrl"]
            self.gas_url = data["gasPriceUrl"]
            self.default_price = data["defaultGasPrice"]

        with open("registrar.abi") as abi:
            self.reg_abi = abi.read()
        with open("registrar.bin") as bin:
            self.reg_bytecode = bin.read()
        with open("payments.abi") as abi:
            self.pay_abi = abi.read()
        with open("payments.bin") as bin:
            self.pay_bytecode = bin.read()

        with open("registrar.json") as registrar:
            data = load(registrar)
            self.address_reg = data["registrar"]
            self.address_pay = data["payments"]

        with open("first_wallet.json") as wallet:
            data = load(wallet)
            self.private_key = data['private_key']

        self.web3 = Web3(HTTPProvider(self.rpcUrl))
        self.account = self.web3.eth.account.privateKeyToAccount(self.private_key)
        self.contract_pay = self.web3.eth.contract(address = self.address_pay, abi = self.pay_abi)
    
    def convert(self, balance):
        if balance == 0:
            return str(balance) + " poa"
        if balance < 10**3:
            return str(balance) + " wei"
        elif balance < 10**6:
            balance = balance / 10**3
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " kwei"
            return str(balance) + " kwei"
        elif balance < 10**9:
            balance = balance / 10**6
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " mwei"
            return str(balance) + " mwei"
        elif balance < 10**12:
            balance = balance / 10**9
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " gwei"
            return str(balance) + " gwei"
        elif balance < 10**15:
            balance = balance / 10**12
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " szabo"
            return str(balance) + " szabo"
        elif balance < 10**18:
            balance = balance / 10**15
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " finney"
            return str(balance) + " finney"
        else:
            balance = balance / 10**18
            if len(str(balance)) > 8:
                return "{0:.6f}".format(balance).rstrip('0').rstrip(".") + " poa"
            return str(balance) + " poa"

    def make_transaction(self, reciever, value):
        # Получаем текущий баланс пользователя
        balance = self.web3.eth.getBalance(self.account.address)

        # Запрашиваем текущий gas price
        data = requests.get(self.gas_url)
        gas = self.web3.eth.estimateGas({"to": reciever, "from": self.account.address, "value": value})
        if data.status_code != 200:
            gas_price = self.default_price
        else:
            gas_price = int(data.json()["fast"] * 10**9)
        if balance < gas * gas_price:
            print("Not enough funds to send this value")
            return

        # Формируем транзакцию
        tx = {
            "to": reciever,
            "nonce": self.web3.eth.getTransactionCount(self.account.address),
            "gas": gas,
            "gasPrice": gas_price,
            "value": int(value)
        }
        # Подписываем транзакцию
        sign = self.account.signTransaction(tx)
        #Получаем хэш транзакции
        tx_hash = self.web3.eth.sendRawTransaction(sign.rawTransaction)
        # Получаем полную информацию о транзакции
        tx_reciept = self.web3.eth.waitForTransactionReceipt(tx_hash)
        while tx_reciept["status"] != 1:
            sleep(0.1)
            tx_reciept = self.web3.eth.getTransactionReceipt(tx_hash)
    

        # Создаём транзакцию для записи о переводе в смарт - контракт
        tx_pay = {
            "from": self.account.address,
            "nonce": self.web3.eth.getTransactionCount(self.account.address),
            "gas": 1500000,
            "gasPrice": gas_price
        }
        # Извлекаем хэщ транзакции перевода
        tx_bytes = self.web3.toBytes(tx_reciept["transactionHash"])
        # Кладём транзакцию о переводе в контракт
        to_signed_pay = self.contract_pay.functions.add_payment(self.account.address, reciever, tx_bytes).buildTransaction(tx_pay)
        # Подписываем транзакцию
        signed_tx = self.account.signTransaction(to_signed_pay)

        # Получаем хэш транзакции
        pay_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        # Получаем полную информацию о транзакции
        pay_reciept = self.web3.eth.waitForTransactionReceipt(pay_hash)
        while pay_reciept["status"] != 1:
            sleep(0.1)
            pay_reciept = self.web3.eth.getTransactionReceipt(pay_hash)

        print("""Payment of {} to {} scheduled""".format(self.convert(int(value)), reciever))
        print("Transaction Hash:", tx_reciept["transactionHash"].hex())
        print("Your transaction added to your payments list!")
        print("Payment added:", pay_reciept["transactionHash"].hex())

    def show_payments(self):
        payments = self.contract_pay.functions.get_payments_list(self.account.address).call()
        for payment in payments:
            data = self.web3.eth.getTransaction(payment.hex())
            if data["from"] == self.account.address: 
                time_sending = datetime.fromtimestamp(self.web3.eth.getBlock(data["blockNumber"])["timestamp"])
                to = data["to"] #str(contract_reg.functions.get_number(data["to"]).call())
                # to = to[to.find("'") + 1:to.rfind("'")]
                value = self.convert(int(data["value"]))
                print(time_sending, "TO:", to, "VALUE:", value)
            else:
                time_sending = datetime.fromtimestamp(self.web3.eth.getBlock(data["blockNumber"])["timestamp"])
                sender = data["from"] # str(contract_reg.functions.get_number(data["from"]).call())
                # sender = sender[sender.find("'") + 1:sender.rfind("'")]
                value = self.convert(int(data["value"]))
                print(time_sending, "FROM:", sender, "VALUE:", value)

    def get_balance(self):
        balance = self.web3.eth.getBalance(self.account.address)
        print("Your balance is", balance)


manager = AccountManager()
manager.make_transaction('0xa118daF3d5451f5fA014048CFf5d6baD4ab5c9BE', 2000000000)
manager.show_payments()