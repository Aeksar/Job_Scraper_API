from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Annotated


class MongoConfig(BaseSettings):
    HOST: Annotated[str, Field(validation_alias="MONGO_HOST")]
    PORT: Annotated[int, Field(validation_alias="MONGO_PORT")]
    DB: Annotated[str, Field(validation_alias="MONGO_DB")]
    TEST_DB: Annotated[str, Field(validation_alias="MONGO_TEST_DB")]
    USER: Annotated[str, Field(validation_alias="MONGO_USER")]
    PASSWORD: Annotated[str, Field(validation_alias="MONGO_PASSWORD")]
    
    def url(self):
        return f"mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore',
        env_file_encoding='utf-8',
    )
        
        
class RabbitConfig(BaseSettings):
    HOST: Annotated[str, Field(validation_alias="RMQ_HOST")]
    PORT: Annotated[int, Field(validation_alias="RMQ_PORT")]
    USER: Annotated[str, Field(validation_alias="RMQ_USER")]
    PASSWORD: Annotated[str, Field(validation_alias="RMQ_PASSWORD")]
    PRODUCE_QUEUE: Annotated[str, Field(validation_alias="RMQ_PRODUCE_QUEUE")]
    CONSUME_QUEUE: Annotated[str, Field(validation_alias="RMQ_CONSUME_QUEUE")]
    
    def url(self):
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore',
        env_file_encoding='utf-8',
    )