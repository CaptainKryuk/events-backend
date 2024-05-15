from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	# ROOT_DIR: Path = get_project_root()


	# CORS origins
	CORS_ORIGINS: list[str] | str = '*'

	ENV: str = 'production'
	DEBUG: bool = False
	SERVICE_NAME: str = ''
	SERVICE_SLUG: str = ''
	VERSION: str = 'local'

	# POSTGRESQL
	POSTGRESQL_HOST: str = 'localhost'
	POSTGRESQL_USER: str = 'root'
	POSTGRESQL_PASSWORD: str = 'pass'
	POSTGRESQL_DATABASE: str = 'db'
	POSTGRESQL_PORT: str = '5432'

	model_config = SettingsConfigDict(
		env_file='.env', env_file_encoding='utf-8', extra='allow', case_sensitive=True
	)
