from marketsimulator.config.settings import Settings


def test_settings_defaults():
    settings = Settings()

    assert settings.app_name == "marketsimulator"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
