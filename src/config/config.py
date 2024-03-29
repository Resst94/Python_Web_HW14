from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str = "db"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_port: int = 5432
    sqlalchemy_database_url: str = "postgresql+psycopg2://postgres:password@localhost:5432/database"
    secret_key: str = "1234567890"
    algorithm: str = "HS256"
    mail_username: EmailStr = "postgres@meail.com"
    mail_password: str = "postgres"
    mail_from: EmailStr = "user@example.com"
    mail_port: int = 465
    mail_server: str = "postgres"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str | None = None
    cloudinary_name: str = 'abc'
    cloudinary_api_key: int = 326488457974591
    cloudinary_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()