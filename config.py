import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "Product API")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        self.storage_type = os.getenv("STORAGE_TYPE", "postgres")
        self.json_file_path = os.getenv("JSON_FILE_PATH", "data/products.json")
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = int(os.getenv("POSTGRES_PORT", "5435"))
        self.postgres_user = os.getenv("POSTGRES_USER", "nian")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD", "8203")
        self.postgres_database = os.getenv("POSTGRES_DATABASE", "muhoco")

        self.sftp_host = os.getenv("SFTP_HOST", "localhost")
        self.sftp_port = int(os.getenv("SFTP_PORT", "22"))
        self.sftp_username = os.getenv("SFTP_USERNAME", "")
        self.sftp_password = os.getenv("SFTP_PASSWORD", "")

        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        self.smtp_tls = os.getenv("SMTP_TLS", "true").lower() == "true"

        self.attachment_max_size_mb = int(os.getenv("ATTACHMENT_MAX_SIZE_MB", "50"))
        self.attachment_allowed_types = os.getenv(
            "ATTACHMENT_ALLOWED_TYPES", ".xlsx,.xls,.csv,.pdf"
        ).lower().split(",")

        self.recipients_file_path = os.getenv(
            "RECIPIENTS_FILE_PATH", "notifications/config/recipients.json"
        )

        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_from_number = os.getenv("TWILIO_FROM_NUMBER", "")


def get_settings() -> Settings:
    return Settings()