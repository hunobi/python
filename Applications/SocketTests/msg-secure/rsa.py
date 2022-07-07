from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def get_pair_key():
    keyPair = RSA.generate(2048)
    pubKey = keyPair.publickey()
    public = pubKey.exportKey()
    private = keyPair.exportKey()
    return private, public


def encrypt(key, msg):
    public = RSA.import_key(key)
    encryptor = PKCS1_OAEP.new(public)
    return encryptor.encrypt(msg)



def decrypt(key, s_msg):
    private = RSA.import_key(key)
    decryptor = PKCS1_OAEP.new(private)
    return decryptor.decrypt(s_msg)
