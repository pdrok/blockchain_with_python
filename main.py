# main.py
"""
A simple Blockchain in Python
https://geekflare.com/create-a-blockchain-with-python/
"""
import hashlib

class GeekCoinBlock:

    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        """
        self.chain - The list where all block are recorded. We can access each block via list
        indexes.
        """
        self.chain = []
        self.generate_genesis_block()
    """
    Append the genesis or fist block to the chain. The previous hash of the block is "0", and
    the list of transactions is simply "Genesis Block."
    """
    def generate_genesis_block(self):
        self.chain.append(GeekCoinBlock("0", ['Genesis Block']))
    """
    This allow us to append blocks to the chain with just a list of transactions. It would be
    very annoying to create a block manually every time we want to record a transaction
    """
    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(GeekCoinBlock(previous_block_hash, transaction_list))
    """
    Print the chain of block with a for loop
    """
    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")
    
    """
    A property that lets us access the last element of the chain. We used it on the
    create_block_from_transaction method.
    """
    @property
    def last_block(self):
        return self.chain[-1]       

t1 = "George sends 3.1 GC to Joe"
t2 = "Joe sends 2.5 GC to Adam"
t3 = "Adam sends 1.2 GC to Bob"
t4 = "Bod sends 0.4 GC to Charlie"
t5 = "Charlie sends 0.2 GC to David"
t6 = "David sends 0.1 GC to Eric"

myblockchain = Blockchain()

myblockchain.create_block_from_transaction([t1, t2])
myblockchain.create_block_from_transaction([t3, t4])
myblockchain.create_block_from_transaction([t5, t6])

myblockchain.display_chain()

