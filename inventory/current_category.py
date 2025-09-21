import logging

from django.contrib.auth.models import User
from django.core.cache import cache


logger = logging.getLogger(__name__)


CURRENT_CATEGORY_CACHE_KEY_PREFIX = 'current_category_slug'
CURRENT_CATEGORY_CACHE_TIMEOUT = 60 * 60 * 24 * 14  # 2 weeks


def current_category_cache_key(user: User) -> str:
    return f'{CURRENT_CATEGORY_CACHE_KEY_PREFIX}_{user.pk}'


def set_current_category_slug(*, user: User, slug: str | None):
    key = current_category_cache_key(user)
    logger.info('Setting current category slug=%r with key=%r', slug, key)
    cache.set(key, slug, timeout=CURRENT_CATEGORY_CACHE_TIMEOUT)


def get_current_category_slug(*, user: User) -> str | None:
    key = current_category_cache_key(user)
    slug = cache.get(key)
    logger.info('Getting current category from key=%r -> slug=%r', key, slug)
    return slug
