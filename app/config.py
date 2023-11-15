from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pghost: str = 'localhost'
    postgres_user: str = 'postgres'
    pgport: str = '5432'
    postgres_password: str = 'postgres'
    pgdatabase: str = 'jobetude'
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 180
    cloudinary_cloud_name: str = 'cloud_name'
    cloudinary_api_secret: str = 'api_secret'
    cloudinary_api_key: str = 'api_key'
    
    
    class Config:
        env_file = '.env'
        
settings = Settings()