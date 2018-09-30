import hashlib
import json
import datetime

class Transaction:
    
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount


class Block:
    
    def __init__(self, timestamp, transactions, previousHash = ''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()
    
    #calculate SHA256 HASH
    def calculateHash(self):
        transactionsArray = []
        if isinstance(self.transactions, list):
            for trans in self.transactions:
                transactionsArray.append(trans.__dict__)
            transactionsJsonString = json.dumps(transactionsArray)
        else:
            transactionsJsonString = json.dumps(self.transactions.__dict__)
        return hashlib.sha256((self.previousHash + self.timestamp + transactionsJsonString + str(self.nonce)).encode()).hexdigest()
    
    def mineBlock(self,difficulty):
        # increment nonce until the hash does not begin with sufficient number of 0s
        while(self.hash[0: difficulty] != '0'*difficulty):
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        print("Block mined " + self.hash)


class Blockchain:
    
    def __init__(self, difficulty):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = difficulty
        self.pendingTransactions = []
        self.miningReward = 1
    
    #create the first block, also called genesis block
    def createGenesisBlock(self):
        return Block("01/01/1990", Transaction(None, None, 0), "0")
    
    #get last block in the chain
    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]
    
    def minePendingTransactions(self, miningRewardAddress):
        # add miner address to the list of transactions to receive the reward
        self.pendingTransactions.append(Transaction(None, miningRewardAddress, self.miningReward))
        block = Block(str(datetime.date.today()), self.pendingTransactions, self.getLatestBlock().hash)
        block.mineBlock(self.difficulty)
        print("Block successfully mined")
        print("Reward credited to your wallet")
        print("Check your balance")
        self.chain.append(block)
        self.pendingTransactions = []
        
    def createTransaction(self, transaction):
            self.pendingTransactions.append(transaction)
            
    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            if isinstance(block.transactions, list):
                for trans in block.transactions:
                    if trans.fromAddress == address:
                        balance = balance - trans.amount
                    if trans.toAddress == address:
                        balance = balance + trans.amount
            else:
                if block.transactions.fromAddress == address:
                    balance = balance - block.transactions.amount
                if block.transactions.toAddress == address:
                    balance = balance + block.transactions.amount
        return balance
            
    def isChainValid(self):
        for i in range(1, len(self.chain)-1):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]
            if currentBlock.hash != currentBlock.calculateHash():
                print("Data on the blockchain is tampered")
                return False
            if currentBlock.previousHash != previousBlock.hash:
                print("Hash of previous block does not match the previous hash of current block")
                return False
        return True


class User_actions:
    def __init__(self):
        self.difficulty = 0
        self.blockcoin = None

    def createBlockchain(self):
        self.difficulty = int(input("Enter difficulty from 0 to 5: "))
        self.blockcoin = Blockchain(self.difficulty)
        print("Created new blockchain with genesis block")
    
    def createTransaction(self):
        if self.blockcoin is not None:
            fromAddress = input("Enter sender's address: ")
            toAddress = input("Enter receiver's address: ")
            amount = int(input("Enter amount: "))
            currentTransaction = Transaction(fromAddress,toAddress, amount)
            self.blockcoin.createTransaction(currentTransaction)
            print("Transaction added to pending stack")
        else:
            print("Blockchain doesn't exist. Please create one.")

    def minePendingTransactions(self):
        if self.blockcoin is not None:
            if len(self.blockcoin.pendingTransactions) != 0:
                miningRewardAddress = input("Enter address to transfer money on successful mining: ")
                self.blockcoin.minePendingTransactions(miningRewardAddress)
            else:
                print("No transactions are pending")
        else:
            print("Blockchain doesn't exist. Please create one")

    def viewBlockchain(self):
        if self.blockcoin is not None:
            for block in self.blockcoin.chain:
                print(json.dumps(block, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        else:
            print("Blockchain doesn't exist. Please create one.")
    
    def checkBlockchainValid(self):
        if self.blockcoin is not None:
            print("Is chain valid? " + str(self.blockcoin.isChainValid()))
        else:
            print("Blockchain doesn't exist. Please create one.")
    
    def getBalanceOfAddress(self):
        address = input("Enter address to get balance for: ")
        print("Balance is: " + self.blockcoin.getBalanceOfAddress(address))
        

if __name__ == '__main__':
    currentUser = User_actions()
    choice = 1
    while(choice != 0):
        print("\n Select appropriate option:")
        print("1. Create a new blockchain")
        print("2. Create a transaction to be added to the blockchain")
        print("3. Mine pending transactions")
        print("4. View blockchain")
        print("5. Attempt to change block on the blockchain")
        print("6. Check if blockchain is valid")
        print("7. Get balance of address")
        print("0. Exit")
        choice = int(input())
        print("\n")
        if choice == 1:
            currentUser.createBlockchain()
        elif choice == 2:
            currentUser.createTransaction()
        elif choice == 3:
            currentUser.minePendingTransactions()
        elif choice == 4:
            currentUser.viewBlockchain()
        elif choice == 5:
            # todo
            # need idea to implement
            print("Pending")
        elif choice == 6:
            currentUser.checkBlockchainValid()
        elif choice == 7:
            currentUser.getBalanceOfAddress()