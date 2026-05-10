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