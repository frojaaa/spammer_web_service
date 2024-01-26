from fastapi import APIRouter

from . import accounts
from . import chats
from . import proxies
from . import subscriptions
from . import projects


router = APIRouter()

router.include_router(projects.router)
router.include_router(accounts.router)
router.include_router(chats.router)
router.include_router(proxies.router)
router.include_router(subscriptions.router)
