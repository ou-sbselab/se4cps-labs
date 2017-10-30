# Two users encrypting/decrypting messages to/from each other
# Sample modified from http://coding4streetcred.com/blog/post/Asymmetric-Encryption-Revisited-(in-PyCrypto)
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
 
# Use a larger key length in practice...
KEY_LENGTH = 1024  # Key size (in bits)
random_gen = Random.new().read
 
# Generate RSA private/public key pairs for both parties...
keypair_userA = RSA.generate(KEY_LENGTH, random_gen)
keypair_userB = RSA.generate(KEY_LENGTH, random_gen)
 
# Public key export for exchange between parties...
pubkey_userA = keypair_userA.publickey()
pubkey_userB = keypair_userB.publickey()
 
# Plain text messages...
message_to_userA  = "This is a message from User B"
message_to_userB  = "Thanks User A.  It was nice of you to send that message"
 
# Generate digital signatures using private keys...
hash_of_userA_message = MD5.new(message_to_userA).digest()
signature_userB       = keypair_userB.sign(hash_of_userA_message, '')
hash_of_userB_message = MD5.new(message_to_userB).digest()
signature_userA       = keypair_userA.sign(hash_of_userB_message, '')
 
# Encrypt messages using the other party's public key...
encrypted_for_userA = pubkey_userA.encrypt(message_to_userA, 32) #from UserB
encrypted_for_userB = pubkey_userB.encrypt(message_to_userB, 32) #from UserA
 
# Decrypt messages using own private keys...
decrypted_userA = keypair_userA.decrypt(encrypted_for_userA)
decrypted_userB = keypair_userB.decrypt(encrypted_for_userB)
 
# Signature validation and console output...
hash_userA_decrypted = MD5.new(decrypted_userA).digest()
if pubkey_userB.verify(hash_userA_decrypted, signature_userB):
    print "User A received from User B:"
    print decrypted_userA
    print ""
 
hash_userB_decrypted = MD5.new(decrypted_userB).digest()
if pubkey_userA.verify(hash_userB_decrypted, signature_userA):
   print "User B received from User A:"
   print decrypted_userB

