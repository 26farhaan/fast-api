from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    my_secret_key: str = ''
    jwt_algorithm: str = ''

    class Config:
        env_file = ".env"


settings = Settings()
