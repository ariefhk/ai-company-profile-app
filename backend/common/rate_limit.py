from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import get_configs

configs = get_configs()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[configs.RATE_LIMIT_DEFAULT],
    storage_uri="memory://",
)
