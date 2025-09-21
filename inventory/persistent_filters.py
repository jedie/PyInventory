import logging

from django.contrib import admin
from django.core.cache import cache
from django.db.models.options import Options


logger = logging.getLogger(__name__)


CURRENT_CATEGORY_CACHE_KEY_PREFIX = 'persistent_parameter'
CURRENT_CATEGORY_CACHE_TIMEOUT = 60 * 60 * 24 * 14  # 2 weeks


def persistent_parameter(request, opts: Options, parameter_name: str):
    cache_key = (
        f'{CURRENT_CATEGORY_CACHE_KEY_PREFIX}_{request.user.pk}_{opts.app_label}_{opts.model_name}_{parameter_name}'
    )

    # Collect from GET:
    if parameter_name in request.GET:
        current_value = request.GET[parameter_name] or None
        logger.debug('Store %r to %r', current_value, cache_key)
        cache.set(cache_key, current_value, timeout=CURRENT_CATEGORY_CACHE_TIMEOUT)
        return current_value

    # Try to restore from cache:
    current_value = cache.get(cache_key)
    logger.debug('Restore %r from %r', current_value, cache_key)
    return current_value


class PersistentRelatedFieldListFilter(admin.RelatedFieldListFilter):
    """
    Stores the last filter value in the cache and restores it on next visit.
    Note: Will not restore "is null" filter state!
    """

    def __init__(self, field, request, params, model, model_admin, field_path):
        opts: Options = model._meta
        super().__init__(field, request, params, model, model_admin, field_path)

        current_parameter = persistent_parameter(request, opts, parameter_name=self.lookup_kwarg)
        if current_parameter and not self.lookup_val:
            logger.info('Restore %r filter for %s with %r', field_path, opts.model_name, current_parameter)
            self.lookup_val = [current_parameter]
            self.used_parameters = {self.lookup_kwarg: self.lookup_val}
