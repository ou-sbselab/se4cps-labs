from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack

bs  = Blowfish.block_size
key = "CSCI5900 -- again what a great key." 
plaintext = "This is some new plaintext with a different way of handling the padding issue."

iv = Random.new().read(bs)
cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
plen = bs - divmod(len(plaintext), bs)[1]
padding = [plen] * plen
padding = pack('b'*plen, *padding)
msg = iv + cipher.encrypt(plaintext + padding)

# Output
print "Pre-encryption  [%s]" % plaintext
print "Post-encryption [%s]" % msg

# Now decrypt
decrypted = cipher.decrypt(msg)
print "Decrypted 1     [%s]" % decrypted

# Oops, what happened here? 
iv     = msg[:bs]
msg    = msg[bs:]
cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
msg    = cipher.decrypt(msg)
last_byte = msg[-1]
msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
print "Decrypted 2     [%s]" % repr(msg)


# sources:
# https://www.dlitz.net/software/pycrypto/api/current/
# https://stackoverflow.com/questions/35042164/how-to-decrypt-using-blowfish-in-pycrypto
