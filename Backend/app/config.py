# config setup, everything comes from the env file  

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # aws-s3 storage configs 
   
    s3_storage_access_key_id: str
    s3_storage_secret_access_key: str
    s3_storage_bucket_name: str
    s3_storage_region: str 
   

    # gemini part used for scoring pronunciation 
    openrouter_api_key: str
    openrouter_model: str = "qwen/qwen3-32b"


    # faster-whisper fixed settings 
    whisper_model_size: str = "small.en"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"


    # rules and restrictions 
    min_audio_seconds: float = 30.0
    max_audio_seconds: float = 45.0
    data_retention_hours: int = 48



    # frontend settings 
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()



