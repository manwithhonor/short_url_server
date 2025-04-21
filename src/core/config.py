from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    project_host: str
    project_port: int
    black_list: list = [
        # "127.0.0.1",
        "56.24.15.106"
    ]

    class Config:
        env_file = '.env'


app_settings = AppSettings()
