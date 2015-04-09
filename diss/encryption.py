
import os
import hashlib
from Crypto.Cipher import AES

from .settings import STORAGE_PATH, TMPSTORAGE_PATH


def copy_and_encrypt(filepath, key):
    "Encrypt the file into the data store, and returns its id."

    tmp_name = 'RANDOM_STUFF'
    tmp_destination = os.path.join(TMPSTORAGE_PATH, tmp_name)

    #for



    open(tmp_destination, 'wb').write(open(filepath, 'rb').read())

    enc_hash = 'ENC_HASH_1234567890'

    # Now that we have the hash of the encrypted file, move the
    # encrypted file to the storage and return the hash.

    destination = os.path.join(STORAGE_PATH, enc_hash)
    os.rename(tmp_destination, destination)

    return enc_hash
