from celery.utils.log import get_task_logger
from otp.operator import FactorySMS
from random import randint
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from config.celery import app

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
logger = get_task_logger(__name__)


@app.task(bind=True)
def send_otp_task(self, user_id, operator_path):

    code = randint(1000,9999)
    result = "{} {}".format(code,user_id)
    cache.set("code{}".format(user_id) ,result,timeout=CACHE_TTL)

    try:
        return FactorySMS().get_sms(operator_path).sms_sender()
    except:
        app.control.revoke(self.request.id, terminate=True)