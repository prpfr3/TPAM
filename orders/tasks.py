from celery import shared_task
import logging
from django.core.mail import send_mail
from django.conf import settings

from .models import Order

logger = logging.getLogger(__name__)


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (
        f"Dear {order.first_name},\n\n"
        f"You have successfully placed an order."
        f"Your order ID is {order.id}."
    )

    try:
        logger.info(f"Sending email to {[order.email]}...")  # Log task start
        logger.debug(f"Email subject: {subject}")
        logger.debug(f"Email message: {message}")
        mail_sent = send_mail(
            subject, message, "paul.frost@talktalk.net", [order.email]
        )
        logger.info(f"Email sent successfully to {[order.email]}.")  # Log success
    except Exception as e:
        logger.error(f"Error sending email to {[order.email]}: {e}")  # Log errors
        raise e

    return mail_sent
