from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CLOUDKAFKA_BROKERS: str
    CLOUDKAFKA_USERNAME: str
    CLOUDKAFKA_PASSWORD: str

    KAFKA_CONSUMER_GROUP: str
    KAFKA_APP_NAME: str
    KAFKA_DEFAULT_TOPIC: str
    KAFKA_GROUP_ID: str
    KAFKA_VALUE_SERIALIZER: str

    ZEEBE_ADDRESS: str
    ZEEBE_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
