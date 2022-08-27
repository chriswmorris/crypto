from Crypto.Cipher import AES
import binascii, os


'''
A simple script demonstrating AES-GCM

For demonstration purposes. Do not use in production, key is written as plaintext. 

Encrypted Object  = IV/Nonce + Ciphertext + AuthTag

'''

print("===============================")
print("AES-GCM Decryption")
print("===============================")

buffer = 1024 * 1024

#Open Files
key = open("key.bin","rb")
key = key.read()
encryptedfile = open("encrypted.enc","rb")
decryptedfile = open("decrypted.txt","wb")

print("Key: "  + str(binascii.hexlify(key).decode("utf-8")))

#Get IV from the start of the file
iv = encryptedfile.read(16) 
print("IV: " + str(binascii.hexlify(iv).decode("utf-8")))
decryptor = AES.new(key, AES.MODE_GCM, nonce=iv)


#Get 
filesize = os.path.getsize("encrypted.enc")
encryptedsize = filesize - 16 - 16  

#Decrypt and save to file
for _ in range(int(encryptedsize / buffer)):
    encrypteddata = encryptedfile.read(buffer)  
    decrypteddata = decryptor.decrypt(encrypteddata)
    decryptedfile.write(decrypteddata)  
encrypteddata = encryptedfile.read(int(encryptedsize % buffer))  
decrypteddata = decryptor.decrypt(encrypteddata)  
decryptedfile.write(decrypteddata)  

# Verify AuthTag at the end
authtag = encryptedfile.read(16)
print("AuthTag: " + str(binascii.hexlify(authtag).decode("utf-8")))
try:
    decryptor.verify(authtag)
except ValueError as error:
    
    encryptedfile.close()
    decryptedfile.close()
    print("Not verified, do not use")
    raise error

encryptedfile.close()
decryptedfile.close()
