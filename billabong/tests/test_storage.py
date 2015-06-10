
from billabong import add_file
from billabong.settings import inventory, storage


def test_list_blobs():
    meta = add_file('hello.txt', key=b'0'*32)
    assert meta
    blobs = list(storage.list_blob_ids())
    assert blobs
    assert len(blobs) > 1

    inventory.delete(meta['id'])
    storage.delete(meta['blob'])
