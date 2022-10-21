import numpy as np
from textwrap import wrap
from copy import deepcopy
import pandas as pd

class AES():

  def __init__(self, plainTextFile="input.pt", keyFile="key.key"):
    #Reading our key from the file
    with open(keyFile, 'r') as filekey:
      key = filekey.read()

    #Reading our plainText from the file
    with open(plainTextFile, 'r') as inputFile:
      plainText = inputFile.readlines()
    for i in range(len(plainText)):
      plainText[i] = plainText[i].strip()
      plainText[i] = plainText[i].replace(" ", "")
    # Preprocessing to remove unnecessary stuff
    key = key.replace(" ", "")

    # Converting our text and key to 4x4 numpy arrays
    # plainText = self.stringToArray(plainText)
    # key = self.stringToArray(key)
    self.plainText = plainText
    self.key = key
    self.keys = []
    self.cipherText = []

    # Creating our sBox dataframes here for byte substitution
    self.sBox = pd.read_table(r"rijndael-box.txt", delimiter="\t")
    self.sBox = self.sBox.set_index('Unnamed: 0')
    self.inverseSBox = pd.read_table(r"inverse-rijndael-box.txt",
                                     delimiter="\t")
    # print(self.inverseSBox.loc['F','F'])
    self.rCon = pd.read_table(r"rcon.txt", delimiter="\t")
    self.rCon = list(self.rCon.loc[0])
    self.rCon = [str(i) for i in self.rCon]

  def addRoundKey(self, state, key):
    for i in range(len(state)):
      for j in range(len(state)):
        state[i][j] = f'{(int(state[i][j], 16) ^ int(key[i][j], 16)):x}'
    return self.padZeros(state, dtype='arr')

  def addRoundKeyExpansion(self, state, key):
    # # Converting our 4x4 state arrays to strings for manipulation
    # state = self.arrayToString(state)
    # key = self.arrayToString(key)

    # # To convert hexadecimal notations to integer and perform xor operation through ^
    # state = int(state, 16) ^ int(key, 16)
    # # To convert integer notations to hexadecimal
    # state = f'{state:x}'
    # # Checking for padding of zeros
    for i in range(len(state)):
      state[i] = f'{(int(state[i], 16) ^ int(key[i], 16)):x}'
    state = self.padZeros(state)
    # Convert back to state array and return
    return state

  def keyExpansion(self, key, round):
    word = key[3]
    word = np.roll(word, -1)
    # print("shi", word)
    for i in range(len(word)):
      word[i] = self.sBox.loc[list(word[i])[0].capitalize(),
                              list(word[i])[1].capitalize()]
    # print("sub", word)
    rcon = np.array([self.rCon[round], "00", "00", "00"])
    # print("r", rcon)
    word = self.addRoundKeyExpansion(rcon, word)
    expandedKey = []
    for words in key:
      # print("xor", word, words)
      word = self.addRoundKeyExpansion(words, word)
      expandedKey.append(word)
    expandedKey = np.array(expandedKey)
    # print(expandedKey)
    return expandedKey

  def byteSubstitution(self, state, sBox):
    # Iterate over each and every index of state and replace with the respective sBox passed
    # Pass the respective sBox for encryption or decryption
    for i in range(len(state)):
      for j in range(len(state)):
        # first index of loc is the row name and second index corresponds to column name
        # print(state[i][j])
        state[i][j] = sBox.loc[list(state[i][j])[0].capitalize(),
                               list(state[i][j])[1].capitalize()]
    return self.padZeros(state, dtype='np')

  def shiftRows(self, state, count):
    counter = 0
    for i in range(count):
      state[i] = np.roll(state[i], counter)
      counter -= 1
    return self.padZeros(state, dtype='np')

  def mixColumns(self, state, inverse=False):

    def GM(a, b):
      # Multiplication in GF(2**8)
      p = 0
      h = 0
      for i in range(8):
        if b & 1 == 1:
          p ^= a
        h = a & 128
        a <<= 1
        if h == 128:
          a ^= 27
        b >>= 1
      return p % 256

    if inverse:
      # Predefined Matrix
      PM = np.array([[0x0E, 0x0B, 0x0D, 0x09], [0x09, 0x0E, 0x0B, 0x0D],
                     [0x0D, 0x09, 0x0E, 0x0B], [0x0B, 0x0D, 0x09, 0x0E]])
    else:
      PM = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])

    result = np.zeros((4, 4), dtype=int)

    # Multiplying with XOR in galois field(2^3)
    for i in range(4):
      for j in range(4):
        for k in range(4):
          result[i][j] ^= GM(PM[i][k], int(state[k][j], 16))
    for i in range(4):
      for j in range(4):
        state[i][j] = f'{result[i][j]:x}'
    return self.padZeros(state, dtype="arr")

  def encryption(self):# self.keyExpansion()
        print("\nEncryption Phase starting here\n")
        count = 1
        for line in self.plainText:
            print("\nEncrypting Block ", count)
            count += 1
            key = self.stringToArray(self.key)
            # print(self.key)
            state = self.stringToArray(line)
            keys = []
            keys.append(deepcopy(key))
            state = self.addRoundKey(state.T, key.T)
            for i in range(10):
                print("\nRound: ", i)
                state = self.byteSubstitution(state, self.sBox)
                state = self.shiftRows(state, 4)
                if i != 9:
                    state = self.mixColumns(state)
                key = self.keyExpansion(key, i)
                state = self.addRoundKey(state, key.T)
                print("Key for Round " + str(i + 1) + ":  \n", key)
                print("State for Round " + str(i + 1) + ":  \n", state)
                keys.append(deepcopy(key))
            self.keys.append(deepcopy(keys))
            self.cipherText.append(state)
            with open('encryption.enc', 'a') as fileencrypt:
                fileencrypt.write(self.arrayToString(state) + '\n')
        # self.key = key
        print("Final CipherText after encryption:\n", self.cipherText)
        # return self.shiftRows(self.plainText)

  def decryption(self):
    # print("Decryption")
    # print(self.cipherText)
    self.plainText = []
    print("\nDecryption Phase starting here\n")
    for line in self.cipherText:
      state = line
      # print(state)
      count = 0
      print("\nDecrypting Block ", count + 1) 
      key = self.keys[count][-1] #w(40,43)
      # print("Decryption Key:\n",key,"\n")
    
      # Add round key
      state = self.addRoundKey(state, key.T)  
      for i in range(10):
        print("\nRound: ", i)
        #Shift rows
        state = self.shiftRows(state, 4) 
        #Sub bytes
        state = self.byteSubstitution(state, self.inverseSBox)
        #Inverse Mix Cols
        if i != 9:
          state = self.mixColumns(state, inverse=True)
        #Add round key
        key = self.keys[count][-i - 2]
        state = self.addRoundKey(state, key.T)
        print("Key for Round " + str(i + 1) + ":  \n", key)                
        print("State for Round " + str(i + 1) + ":  \n", state)
      self.plainText.append(state)
      with open('decryption.dec', 'a') as filedecrypt:
        filedecrypt.writelines(self.arrayToString(state) + '\n')
      count += 1
    print("Final plainText after decryption:\n", self.plainText)

  # Function to check if zero padding is required, specify dtype as np if 4x4 array is passed, default dtype is str
  def padZeros(self, state, dtype='str'):
    # If default dtype, then only append 0s to string till length is 32
    if dtype == 'str':
      # state = self.stringToArray(state)
      for i in range(len(state)):
        while len(state[i]) < 2:
          state[i] = '0' + state[i]
      # state = self.arrayToString(state)
      # while len(state) < 8:
      #     state = state + '0'
      return state
    # If np array passed, first convert to string, append 0s till 32 length then convert back to array
    elif dtype == 'np':
      state = self.arrayToString(state)
      while len(state) < 32:
        state = state + '0'
      return self.stringToArray(state)
    elif dtype == 'arr':
      for i in range(len(state)):
        for j in range(len(state)):
          while len(state[i][j]) < 2:
            state[i][j] = '0' + state[i][j]
      return state

  # Function to convert from string notation to 4x4 numpy array
  def stringToArray(self, state):
    return np.array(wrap(state, 2)).reshape(4, 4)

  # Function to convert from 4x4 numpy array to string notation
  def arrayToString(self, state):
    return "".join(["".join(item) for item in state.astype(str)])


AESObject = AES()
AESObject.encryption()
AESObject.decryption()
