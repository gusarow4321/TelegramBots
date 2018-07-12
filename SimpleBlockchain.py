# coding: utf-8

import hashlib as hasher
from _datetime import datetime


class Block:
    def __init__(self, ind, timestamp, data, previous_hash):
        self.index = ind
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("utf-8"))
        return sha.hexdigest()


def create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")


def next_block(last):
    return Block(last.index + 1, datetime.now(), f"Hello I'm block {last.index + 1}", last.hash)


blockchain = [create_genesis_block()]

previous_block = blockchain[0]

count_blocks_to_add = 200

for i in range(count_blocks_to_add):
    append_block = next_block(previous_block)
    blockchain.append(append_block)
    previous_block = append_block
    print(f"Block #{append_block.index} has been added to the blockchain!")
    print(f"Hash: {append_block.hash}\n")
