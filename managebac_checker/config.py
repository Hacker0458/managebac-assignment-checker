"""配置加载与验证工具。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional
import os


_TRUE_VALUES = {"1", "true", "t", "yes", "y", "on"}


def _as_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in _TRUE_VALUES


def _as_int(value: Optional[str], default: int) -> int:
    if value is None:
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


def _as_float(value: Optional[str], default: float) -> float:
    if value is None:
        return default
    try:
        return float(value.strip())
    except ValueError:
        return default


def _as_list(value: Optional[str], default: Iterable[str]) -> List[str]:
    if value is None:
        return list(default)
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or list(default)


@dataclass(slots=True)
class Config:
    email: str = ""
    password: str = ""
    url: str = "https://shtcs.managebac.cn"
    headless: bool = True
    timeout: int = 30_000
    debug: bool = False
    report_formats: List[str] = field(default_factory=lambda: ["console", "json"])
    output_dir: Path = Path("./reports")
    enable_notifications: bool = False
    smtp_server: str = ""
    smtp_port: int = 587
    email_user: str = ""
    email_password: str = ""
    notification_email: str = ""
    days_ahead: int = 7
    priority_keywords: List[str] = field(
        default_factory=lambda: ["exam", "test", "project", "essay"]
    )
    fetch_details: bool = False
    details_limit: int = 8
    max_retries: int = 3
    retry_delay_ms: int = 2000
    browser_args: List[str] = field(
        default_factory=lambda: ["--no-sandbox", "--disable-dev-shm-usage"]
    )
    language: str = "zh"
    log_level: str = "INFO"
    log_file: str = "managebac_checker.log"
    interactive: bool = False
    ai_enabled: bool = False
    openai_api_key: str = ""
    ai_model: str = "gpt-3.5-turbo"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 500
    user_agent: str = ""

    @classmethod
    def from_environment(cls, overrides: Optional[dict] = None) -> "Config":
        overrides = overrides or {}
        env = os.environ

        email = overrides.get("email") or env.get("MANAGEBAC_EMAIL")
        password = overrides.get("password") or env.get("MANAGEBAC_PASSWORD")
        if not email or not password:
            raise ValueError("必须提供 MANAGEBAC_EMAIL 和 MANAGEBAC_PASSWORD")

        url = overrides.get("url") or env.get("MANAGEBAC_URL", "https://shtcs.managebac.cn")
        headless = (
            overrides.get("headless")
            if "headless" in overrides
            else _as_bool(env.get("HEADLESS"), True)
        )
        timeout = overrides.get("timeout") or _as_int(env.get("TIMEOUT"), 30_000)
        debug = (
            overrides.get("debug") if "debug" in overrides else _as_bool(env.get("DEBUG"), False)
        )
        language = overrides.get("language") or env.get("LANGUAGE", "zh")
        log_level = overrides.get("log_level") or env.get("LOG_LEVEL", "INFO")
        log_file = overrides.get("log_file") or env.get("LOG_FILE", "managebac_checker.log")
        interactive = (
            overrides.get("interactive")
            if "interactive" in overrides
            else _as_bool(env.get("INTERACTIVE"), False)
        )

        report_formats = overrides.get("report_format")
        if report_formats is None:
            report_formats = _as_list(env.get("REPORT_FORMAT"), ["console", "json"])
        elif isinstance(report_formats, str):
            report_formats = _as_list(report_formats, ["console", "json"])

        output_dir = Path(
            overrides.get("output_dir") or env.get("OUTPUT_DIR", "./reports")
        ).expanduser()

        enable_notifications = (
            overrides.get("enable_notifications")
            if "enable_notifications" in overrides
            else _as_bool(env.get("ENABLE_NOTIFICATIONS"), False)
        )
        smtp_server = overrides.get("smtp_server") or env.get("SMTP_SERVER", "")
        smtp_port = overrides.get("smtp_port") or _as_int(env.get("SMTP_PORT"), 587)
        email_user = overrides.get("email_user") or env.get("EMAIL_USER", "")
        email_password = overrides.get("email_password") or env.get("EMAIL_PASSWORD", "")
        notification_email = overrides.get("notification_email") or env.get(
            "NOTIFICATION_EMAIL", ""
        )

        days_ahead = overrides.get("days_ahead") or _as_int(env.get("DAYS_AHEAD"), 7)
        priority_keywords = overrides.get("priority_keywords") or _as_list(
            env.get("PRIORITY_KEYWORDS"), ["exam", "test", "project", "essay"]
        )
        fetch_details = (
            overrides.get("fetch_details")
            if "fetch_details" in overrides
            else _as_bool(env.get("FETCH_DETAILS"), False)
        )
        details_limit = overrides.get("details_limit") or _as_int(env.get("DETAILS_LIMIT"), 8)
        max_retries = overrides.get("max_retries") or _as_int(env.get("MAX_RETRIES"), 3)
        retry_delay_ms = overrides.get("retry_delay") or _as_int(env.get("RETRY_DELAY"), 2000)

        browser_args_value = overrides.get("browser_args") or env.get("BROWSER_ARGS")
        if isinstance(browser_args_value, str):
            browser_args = _as_list(browser_args_value, ["--no-sandbox", "--disable-dev-shm-usage"])
        elif browser_args_value is None:
            browser_args = ["--no-sandbox", "--disable-dev-shm-usage"]
        else:
            browser_args = list(browser_args_value)

        ai_enabled = (
            overrides.get("ai_enabled")
            if "ai_enabled" in overrides
            else _as_bool(env.get("AI_ENABLED"), False)
        )
        openai_api_key = overrides.get("openai_api_key") or env.get("OPENAI_API_KEY", "")
        ai_model = overrides.get("ai_model") or env.get("AI_MODEL", "gpt-3.5-turbo")
        ai_temperature = overrides.get("ai_temperature") or _as_float(
            env.get("AI_TEMPERATURE"), 0.7
        )
        ai_max_tokens = overrides.get("ai_max_tokens") or _as_int(env.get("AI_MAX_TOKENS"), 500)
        user_agent = overrides.get("user_agent") or env.get("USER_AGENT", "")

        config = cls(
            email=email,
            password=password,
            url=url,
            headless=headless,
            timeout=timeout,
            debug=debug,
            report_formats=report_formats,
            output_dir=output_dir,
            enable_notifications=enable_notifications,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            email_user=email_user,
            email_password=email_password,
            notification_email=notification_email,
            days_ahead=days_ahead,
            priority_keywords=priority_keywords,
            fetch_details=fetch_details,
            details_limit=details_limit,
            max_retries=max_retries,
            retry_delay_ms=retry_delay_ms,
            browser_args=browser_args,
            language=language,
            log_level=log_level,
            log_file=log_file,
            interactive=interactive,
            ai_enabled=ai_enabled,
            openai_api_key=openai_api_key,
            ai_model=ai_model,
            ai_temperature=ai_temperature,
            ai_max_tokens=ai_max_tokens,
            user_agent=user_agent,
        )

        config.ensure_directories()
        return config

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        Path("./logs").mkdir(exist_ok=True)
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)

    def get_report_formats(self) -> List[str]:
        return self.report_formats

    def is_notification_enabled(self) -> bool:
        return self.enable_notifications
