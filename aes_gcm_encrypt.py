from Crypto.Cipher import AES
import binascii, os


'''
A simple script demonstrating AES-GCM

For demonstration purposes. Do not use in production, key is written as plaintext

Encrypted Object  = IV/Nonce + Ciphertext + AuthTag

'''

print("===============================")
print("AES-GCM Encryption")
print("===============================")

#Enter the file you want to encrypt here
filename = ""

plaintextfile = open(filename,"rb")
encryptedfile = open("encrypted.enc","wb")
buffer = 1024 * 1024

#Create key
key = os.urandom(32)

#Save key
with open("key.bin", "wb") as keyfile:
    keyfile.write(key)

encryptor= AES.new(key, AES.MODE_GCM) 

#Write IV/nonce at the start
encryptedfile.write(encryptor.nonce)
plaintext = plaintextfile.read(buffer)

#Encrypt
while len(plaintext) != 0:  
    encrypteddata = encryptor.encrypt(plaintext)  
    encryptedfile.write(encrypteddata)  
    plaintext = plaintextfile.read(buffer)  

#Write AuthTag at the end
authtag = encryptor.digest()
encryptedfile.write(authtag)

plaintextfile.close()
encryptedfile.close()


print("Key: "  + str(binascii.hexlify(key).decode("utf-8")))
print("IV: " + str(binascii.hexlify(encryptor.nonce).decode("utf-8")))
print("AuthTag: " + str(binascii.hexlify(authtag).decode("utf-8")))

