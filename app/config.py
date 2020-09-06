import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    listen_host: str
    listen_port: int
    yc_oauth_token: str
    yc_folder_id: str
    data_path: str

    @staticmethod
    def create_from_env() -> 'Config':
        return Config(
            listen_host=os.getenv('LISTEN_HOST', '0.0.0.0'),
            listen_port=int(os.getenv('LISTEN_PORT', 8000)),
            yc_oauth_token=os.getenv('YC_OAUTH_TOKEN'),
            yc_folder_id=os.getenv('YC_FOLDER_ID'),
            data_path=os.getenv('DATA_PATH'),
        )


CONFIG = Config.create_from_env()
