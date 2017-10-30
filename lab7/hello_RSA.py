from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.exportKey('DER')
public_key  = key.publickey().exportKey('DER')

priKey = RSA.importKey(private_key)
pubKey = RSA.importKey(public_key)

plaintext = "THIS. IS. READABLE."
encrypted = pubKey.encrypt(plaintext, 'x')[0]
decrypted = priKey.decrypt(encrypted)

assert(plaintext == decrypted)
print "Plaintext [%s]" % plaintext
print "Decrypted [%s]" % decrypted

# With loving help from SO
# https://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
