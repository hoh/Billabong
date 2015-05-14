
import os
import uuid
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter

from .settings import STORAGE_PATH, TMPSTORAGE_PATH
from .utils import read_in_chunks

hashing = hashlib.sha256


def copy_and_encrypt(filepath, key):
    "Encrypt the file into the data store, and returns its id."

    tmp_name = 'diss-{}'.format(uuid.uuid4())
    tmp_destination = os.path.join(TMPSTORAGE_PATH, tmp_name)

    source_hash = hashing()
    enc_hash = hashing()
    ctr = Counter.new(128)
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)

    source_file = open(filepath, 'rb')
    dest_file = open(tmp_destination, 'wb')

    for chunk in read_in_chunks(source_file):
        source_hash.update(chunk)
        enc_chunk = crypto.encrypt(chunk)
        enc_hash.update(enc_chunk)
        dest_file.write(enc_chunk)

    # Now that we have the hash of the encrypted file, move the
    # encrypted file to the storage and return the hash.

    destination = os.path.join(STORAGE_PATH, enc_hash.hexdigest())
    os.rename(tmp_destination, destination)

    return enc_hash.hexdigest()


def decrypt_blob(id_, key):
    "Decrypt the content of a blob through a generator."
    enc_path = os.path.join(STORAGE_PATH, id_)
    enc_file = open(enc_path, 'rb')

    ctr = Counter.new(128)
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)

    for enc_chunk in read_in_chunks(enc_file):
        chunk = crypto.decrypt(enc_chunk)
        yield chunk
