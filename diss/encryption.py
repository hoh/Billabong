
import os
import uuid
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter

from .settings import (storage, TMPSTORAGE_PATH)
from .utils import read_in_chunks

hashing = hashlib.sha256


def random_key():
    "Return a randomly generated AES key"
    random = Random.new()
    key = random.read(AES.key_size[2])  # 256 bits
    return key


def copy_and_encrypt(filepath, key):
    "Encrypt the file into the data store, and returns its id."

    tmp_name = 'diss-{}'.format(uuid.uuid4())
    tmp_destination = os.path.join(TMPSTORAGE_PATH, tmp_name)

    source_hash = hashing()
    enc_hash = hashing()
    ctr = Counter.new(128)
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)

    with open(filepath, 'rb') as source_file, \
            open(tmp_destination, 'wb') as dest_file:

        for chunk in read_in_chunks(source_file):
            source_hash.update(chunk)
            enc_chunk = crypto.encrypt(chunk)
            enc_hash.update(enc_chunk)
            dest_file.write(enc_chunk)

    # Now that we have the hash of the encrypted file, move the
    # encrypted file to the storage and return the hash.
    id_ = enc_hash.hexdigest()

    with open(tmp_destination, 'rb') as tmp_file:
        storage.import_blob(id_, tmp_file)
    os.remove(tmp_destination)

    return enc_hash.hexdigest()


def counter_for_offset(offset):
    "Return a Counter for the given offset."
    initial_value = 1 + (offset // 16)
    return Counter.new(128, initial_value=initial_value)


def decrypt_blob(blob_id, key, offset=0, length=None):
    "Decrypt the content of a blob through a generator."

    modulo = offset % 16
    # Compute a file offset, might be lower than the real offset
    file_offset = offset - modulo if offset else 0

    end = offset + length if length else None
    ctr = counter_for_offset(offset)

    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)

    chunks_generator = storage.read_in_chunks(blob_id, offset=file_offset,
                                              chunk_size=10)

    for i, enc_chunk in chunks_generator:
        chunk = crypto.decrypt(enc_chunk)

        if end is not None:
            here = offset - modulo + i*10
            if end <= here + 10:
                chunk = chunk[:end - here]
                yield chunk
                break

        if i == 0:
            yield chunk[modulo:]
        else:
            yield chunk
