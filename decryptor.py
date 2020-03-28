from Crypto.Cipher import AES
from hashlib import md5
import base64


def decrypt(data, time):
    data = base64.decodebytes(data.encode())
    aes = AES.new(md5(str(int(time)).encode()).digest(), AES.MODE_ECB)
    return aes.decrypt(data)