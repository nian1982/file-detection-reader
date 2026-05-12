from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SFTP_HOST: str
    SFTP_PORT: int
    SFTP_USER: str
    SFTP_PASS: str
    SFTP_UPLOAD_DIR: str

     # =========================
    # KEYCLOAK
    # =========================

    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_VERIFY_AUDIENCE: bool = False

    # =========================
    # ORACLE
    # =========================

    ORACLE_HOST: str
    ORACLE_PORT: int
    ORACLE_SERVICE_NAME: str
    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_MIN_POOL: int
    ORACLE_MAX_POOL: int

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def KEYCLOAK_ISSUER(self) -> str:
        return (
            f"{self.KEYCLOAK_URL}"
            f"/realms/{self.KEYCLOAK_REALM}"
        )

    @property
    def KEYCLOAK_JWKS_URL(self) -> str:
        return (
            f"{self.KEYCLOAK_ISSUER}"
            f"/protocol/openid-connect/certs"
        )


settings = Settings()
