import pytest


@pytest.fixture()
def url():
    """Return answer to ultimate question."""
    url = "http://172.26.66.74:1026"
    return url