"""
Package for the application.
"""

# import celery
from TPAM.celery import app as celery_app

__all__ = ["celery_app"]
