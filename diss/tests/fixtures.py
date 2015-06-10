
import pytest
from diss import add_file
from diss.settings import inventory, storage


@pytest.fixture
def record(request):
    record = add_file('hello.txt', key=b'0'*32)

    def fin():
        inventory.delete(record['id'])
        storage.delete(record['blob'])
    request.addfinalizer(fin)
    return record
