def pytest_configure(config):
    assert config.getoption("--strict-markers") is not None
