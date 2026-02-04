from dataclasses import dataclass
import os


def _get_env_var(name: str) -> str:
    """Get environment variable or raise an error if not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set")
    return value


@dataclass(frozen=True)
class EmailConfig:
    """Email server configuration."""

    server: str
    port: int
    user: str
    password: str
    sender: str
    recipients: list[str]
    subject: str = "New Daft Listings"


@dataclass(frozen=True)
class DaftSearchConfig:
    """Daft search filter configuration."""

    min_beds: int
    max_beds: int
    min_baths: int
    max_price: int
    cache_file: str


@dataclass(frozen=True)
class DaftAccountConfig:
    """Daft account credentials for automated responses."""

    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    message_text: str


@dataclass(frozen=True)
class AppConfig:
    """Complete application configuration."""

    email: EmailConfig
    daft_search: DaftSearchConfig
    daft_account: DaftAccountConfig


def load_config() -> AppConfig:
    """Load all configuration from environment variables at startup."""
    email = EmailConfig(
        server=_get_env_var("email_server"),
        port=int(_get_env_var("email_port")),
        user=_get_env_var("email_user"),
        password=_get_env_var("email_password"),
        sender=_get_env_var("sender_email"),
        recipients=_get_env_var("recipients").split(","),
    )

    daft_search = DaftSearchConfig(
        min_beds=int(_get_env_var("rent_min_bedroom")),
        max_beds=int(_get_env_var("rent_max_bedroom")),
        min_baths=int(_get_env_var("rent_min_bath")),
        max_price=int(_get_env_var("rent_max_price")),
        cache_file=_get_env_var("cache_file"),
    )

    daft_account = DaftAccountConfig(
        email=_get_env_var("daft_email"),
        password=_get_env_var("daft_password"),
        first_name=_get_env_var("daft_first_name"),
        last_name=_get_env_var("daft_last_name"),
        phone_number=_get_env_var("daft_phone_number"),
        message_text=_get_env_var("daft_text"),
    )

    return AppConfig(
        email=email,
        daft_search=daft_search,
        daft_account=daft_account,
    )
