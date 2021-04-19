#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # Documentation
# 
# ## Classes
# <br />
# 
# | classname | description |
# | :-- | :-- |
# | Client | with functions for sign and identity |
# | Transaction | with functions sender receiver value time signed |
# | Block | with previous_block_hash Nonce and verified_transactions |
# | Blockchain | with last_block_hash and dump_blockchain |
# 
# ## Global Variables
# | variablename | type | description |
# | --- | --- | --- |
# | Mucoins | list | for holding coins |
# | BChain | Blockchain | the given blockchain |

# In[1]:


k = []
for i in range(2):
    e = (input().split(" ",2))
    k.append(e)
for i in k:
#    print('| {} | {} | {} |'.format(*i))


# In[2]:


import hashlib as h
import random as rand
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections
from Crypto.Hash import SHA
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


# # Defining `Client` class

# In[3]:


class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self.__private_key = RSA.generate(1024,random)
        self._public_key = self.__private_key.publickey()
        self.money_ = 0
        self.chain_ = []
    

    @property
    def money(self):
        return self.money_
    
    @money.setter
    def money(self,value):
        self.money_+=value
        return self.money_
    
    @property
    def _sign(self):
        return PKCS1_v1_5.new(self.__private_key)
    
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


# # testing client

# In[4]:


Ujjwal = Client()
print(Ujjwal.identity)
#print(binascii.hexlify(Ujjwal.__private_key.exportKey(format='DER')).decode('ascii'))


# # creating `Transaction` class

# In[5]:


class Transaction:
    def __init__(self,sender,receiver,amount=0): #both sender and receiver will be passed as their respective 
        self.sender = sender
        self.receiver = receiver
        self.value = amount
        self.time = datetime.datetime.now()
        self.signed = None
        
        
    def details(self):
        if(self.sender == "Genesis"):
            identity = 'Genesis'
        else:
            # sender.identity returns a textual version of the sender identity
            identity = self.sender.identity
        return collections.OrderedDict({'sender':identity,'receiver':self.receiver,'value':self.value,'time':self.time})
    
    def check_validity(self):
        print(self.sender.money_,self.value)
        return self.sender.money_>self.value
    
    def sign_transaction(self):
        #generate private key of sender
        private_key = self.sender._Client__private_key
        # signer for signing the data
        signer = PKCS1_v1_5.new(private_key)
        # h as hash of the given details of transaction
        h = SHA.new(str(self.details).encode('utf-8'))
        # signs using signer.sign()
        self.signed = binascii.hexlify(signer.sign(h)).decode('ascii')
        return self.signed
    def __repr__(self):
        r = "\n-------\n"
        for k,v in self.details().items():
            r+="{}:\t{}\n".format(k,v)
        return r
        


# # Defining `Block` 

# In[6]:


last_block_hash = ""
class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""
    
    def __repr__(self):
        r = str("previous block hash = {}\n".format(self.previous_block_hash))
        r += str('Nonce = {}'.format(self.Nonce))
        r+= "\n".join([str(t) for t in self.verified_transactions])
        return r+'\n======='


# # Creating Miners

# miner will take a block, and perform hashing until it gets the given hash with satisfactory value <br>
# 1. create miner ( identity, take block , perform hash, return hashed block with changed nonce and return )
# 

# In[7]:


class Miner:
    def __init__(self):
        random = Crypto.Random.new().read
        self.__private_key = RSA.generate(1024,random)
        self._public_key = self.__private_key.publickey()
    @property
    def _sign(self):
        return PKCS1_v1_5.new(self.__private_key)
    
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    
    def mine(self,block,trans):
        for tr in trans:
            if(tr.check_validity()):
                block.verified_transactions.append(tr)
            else:
                a = input('bypass?:0')
                if(a):
                    block.verified_transactions.append(tr)
        dig = hash(str(block))
        block.Nonce = 0
        count = 0
        while(not str(dig).endswith('11111')):
            block.Nonce+=1
            dig = hash(str(block))
#             count+=1
#             if(count==1000):
#                 print(dig,block.Nonce)
#                 input()
#                 count = 0
        print('success')
        return block.Nonce


# # Defining `Blockchain`

# In[8]:


MuCoins = []
class Blockchain:
    def __init__(self):
        self.last_block_hash = None
        self.genesis_block = None
        self.chain_ = []
        
    @property
    def chain(self):
        return self.chain_
    #this sets the last block hash too
    @chain.setter
    def chain(self,block):
        if(not self.chain_):
            self.genesis_block = block
        self.last_block_hash = hash(block)
        block.previous_block_hash = self.last_block_hash
        self.chain_.append(block)
        return self.chain_
    @property
    def total_number_of_blocks(self):
        return len(self.chain)
    
    #   to print the blockchain
    def dump_blockchain(self):
        print("Number of blocks in the chain :",str(len(self.chain)))
        print("*************************************")
        for x in range(len(self.chain)):
            block_temp = self.chain[x]
            print("block #",x)
            for tr in block_temp.verified_transactions:
                print(tr)
            print("=================")


# ### used __private_key to ensure nobody else other than the object itself can access it

# # testing transaction

# In[9]:


Ujjwal = Client()
Shashwat = Client()
t = Transaction(Ujjwal,Shashwat.identity,10)
for i,v in t.details().items():
    print(i,v)


# In[10]:


sig = t.sign_transaction()
print(sig)


# # transactions list

# In[11]:


class transactions(list):

    def add_transaction(self,t):
        t.sign_transaction()
        self.append(t)


# In[12]:


Trans = transactions()


# # creating more clients

# In[13]:


ajay = Client()
rehman = Client()


# # adding transactions

# In[15]:


Trans.add_transaction(Transaction(ajay,rehman.identity,10))
Trans.add_transaction(Transaction(Ujjwal,rehman.identity,12))
Trans.add_transaction(Transaction(ajay,Shashwat.identity,15))
Trans.add_transaction(Transaction(rehman,Shashwat.identity,55))
Trans.add_transaction(Transaction(Shashwat,Ujjwal.identity,14))
Trans.add_transaction(Transaction(rehman,ajay.identity,10))
Trans.add_transaction(Transaction(ajay,rehman.identity,1))
Trans.add_transaction(Transaction(Shashwat,Ujjwal.identity,14))
Trans.add_transaction(Transaction(rehman,ajay.identity,10))
Trans.add_transaction(Transaction(ajay,rehman.identity,1))


# In[16]:


for tr in Trans:
    print(tr)


# # Genesis block 

# In[17]:


#defining genesis block as block0
block0 = Block()
block0.previous_block_hash = None
block0.Nonce = None
block0.verified_transactions.append(Transaction('Genesis','',0))
digest = hash(str(block0))
last_block_hash = digest
print(last_block_hash,hash(str(block0)))


# In[18]:


print(block0)


# # Creating blockchain

# In[19]:


BChain = Blockchain()


# # mining

# In[20]:


Fred = Miner()


# In[ ]:





# In[ ]:





# ### Adding Blocks

# In[21]:


BChain.chain = block0                     #adding genesis block


# In[22]:


block1 = Block()
block1.previous_block_hash = BChain.last_block_hash
block1.Nonce = None
Fred.mine(block1,Trans)

BChain.chain = block1       #adding transactions


# # print(block1)

# In[23]:


print(block1)


# ### print blockchain

# In[90]:


BChain.dump_blockchain() #for printing the blockchain


# In[ ]:




