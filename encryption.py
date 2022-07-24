from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import ast


class Encryption:
    def encrypt(self, message):
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)

        public_key = key.publickey()

        encryptor = PKCS1_OAEP.new(public_key)
        encrypted = encryptor.encrypt(str.encode(message))

        return encrypted, key

    def decrypt(self, encrypted, key):
        decryptor = PKCS1_OAEP.new(key)
        decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
        return decrypted.decode('utf-8')

