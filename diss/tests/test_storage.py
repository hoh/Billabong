
from diss import add_file
from diss.storage import FolderStorage
from diss.settings import STORAGE_PATH


def test_list_blobs():
    meta = add_file('hello.txt', key=b'0'*32)
    assert meta
    storage = FolderStorage(STORAGE_PATH)
    blobs = list(storage.list_blob_ids())
    assert blobs
    assert len(blobs) > 1
