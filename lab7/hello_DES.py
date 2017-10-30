from Crypto.Cipher import DES

key       = "CSCI5900"
plaintext = "CSCI5900 is a great class.  I think it should run again next year."

# Why is this necessary???
plaintext = "%s " % plaintext
print "Pre:Length of plaintext\t\t[%d]" % len(plaintext)
while ((len(plaintext) % 8) != 0):
  plaintext = "%s " % plaintext
print "Post:Length of plaintext\t[%d]" % len(plaintext)

# Setup DES encryption
des       = DES.new(key, DES.MODE_ECB)
encrypted = des.encrypt(plaintext)

# Output
print "Pre-encryption  [%s]" % plaintext
print "Post-encryption [%s]" % encrypted

# Now decrypt
decrypted = des.decrypt(encrypted)
print "Decrypted       [%s]" % decrypted
