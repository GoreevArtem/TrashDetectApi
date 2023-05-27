from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)