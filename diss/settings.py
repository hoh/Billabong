
from .storage import FolderStorage
from .inventory import FolderInventory

STORAGE_PATH = './data'
TMPSTORAGE_PATH = './tmpdata'
METADATA_PATH = './meta'

REMOTE_LOCATION = './remote'


storage = FolderStorage(STORAGE_PATH)
inventory = FolderInventory(METADATA_PATH)


remote_storages = [
    FolderStorage(REMOTE_LOCATION)
]
