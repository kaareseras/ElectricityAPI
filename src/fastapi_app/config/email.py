import os
import pathlib

from fastapi.background import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.fastapi_app.config.config import get_settings

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", ""),
    MAIL_PORT=os.environ.get("MAIL_PORT", 1025),
    MAIL_SERVER=os.environ.get("MAIL_SERVER", "192.168.1.179"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", False),
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", False),
    MAIL_DEBUG=False,
    MAIL_FROM=os.environ.get("MAIL_FROM", "noreply@test.com"),
    MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", settings.APP_NAME),
    TEMPLATE_FOLDER=pathlib.Path(__file__).parent.parent.parent / "templates",
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", False),
)

fm = FastMail(conf)


async def send_email(
    recipients: list, subject: str, context: dict, template_name: str, background_tasks: BackgroundTasks
):
    message = MessageSchema(subject=subject, recipients=recipients, template_body=context, subtype=MessageType.html)

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
