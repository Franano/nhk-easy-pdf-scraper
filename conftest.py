import pytest
from pages.nhk_home_page import NHKHomePage


@pytest.fixture
def nhk_page(page):
    """Inicializa y abre la página principal de NHK."""
    nhk = NHKHomePage(page)
    nhk.open()
    return nhk