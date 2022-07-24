from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import base64


class Encryption:
    def generate_keys(self):
        modulus_length = 1024
        key = RSA.generate(modulus_length)
        pub_key = key.publickey()
        return key, pub_key

    def encrypt_private_key(self, message, private_key):
        encryptor = PKCS1_OAEP.new(private_key)
        encrypted_msg = encryptor.encrypt(str.encode(message))
        encoded_encrypted_msg = base64.b64encode(encrypted_msg)
        return encoded_encrypted_msg

    def decrypt_public_key(self, encoded_encrypted_msg, public_key):
        encryptor = PKCS1_OAEP.new(public_key)
        decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
        decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
        return decoded_decrypted_msg.decode('utf-8')