from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix="AUTH_")
    email: str
    password: str

    @property
    def auth_data(self) -> dict[str, str]:
        return {"email": self.email, "password": self.password}


class Config(BaseSettings):
    auth: AuthConfig = Field(default_factory=AuthConfig)
