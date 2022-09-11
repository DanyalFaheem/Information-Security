# Initial decryoted Decryption Routine at the start of the program
def decryptionRoutine():
    from cryptography.fernet import Fernet
    # Read key for decryption
    with open('filekey.key', 'rb') as filekey:
        keys = filekey.read()
    # Create our decryptor
    decryptor = Fernet(keys)
    return decryptor
