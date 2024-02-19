from app.config import CONFIG


def pytest_configure(config):
    CONFIG.BASE_URL = "http://testserver"
