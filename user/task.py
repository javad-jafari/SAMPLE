from celery import shared_task
from celery.utils.log import get_task_logger
from user.models import LoginToken
from knox.models import AuthToken



logger = get_task_logger(__name__)


@shared_task
def login_token_agent_task(user_id, digest, agent):

    logger.info("login_token_task")

    dig = AuthToken.objects.get(
            user_id=user_id, 
            digest=digest
            )
        
    LoginToken.objects.create(
            digest=dig, 
            agent=agent)

    return "login"