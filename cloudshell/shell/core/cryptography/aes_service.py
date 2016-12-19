import base64
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    """Encrypt & Decrypt using PyCrypto AES"""

    def __init__(self, key):
        self.key = base64.b64decode(key)
        # AES block size
        self.BLOCK_SIZE = 16

    def encrypt(self, raw):
        """Encrypt using PyCrypto AES"""
        pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        raw = pad(raw)

        iv = Random.new().read(self.BLOCK_SIZE)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        res = iv + cipher.encrypt(raw)
        return base64.b64encode(res)

    def decrypt(self, enc):
        """Decrypt using PyCrypto AES"""
        enc = base64.b64decode(enc)
        iv = enc[:self.BLOCK_SIZE]
        unpad = lambda s: s[:-ord(s[-1])]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[self.BLOCK_SIZE:]))
