import logging
import re

import requests
from django.db import models
from django.template.defaultfilters import striptags
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from urllib3.exceptions import HTTPError

from inventory.models.base import BaseModel


logger = logging.getLogger(__name__)


class BaseLink(BaseModel):
    name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('BaseLink.name.verbose_name'),
        help_text=_('BaseLink.name.help_text')
    )
    url = models.URLField(
        verbose_name=_('Link.url.verbose_name'),
        help_text=_('Link.url.help_text')
    )
    last_check = models.DateField(
        blank=True, null=True, editable=False,
        verbose_name=_('Link.url.verbose_name'),
        help_text=_('Link.url.help_text')
    )
    status_code = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False,
        verbose_name=_('Link.status_code.verbose_name'),
        help_text=_('Link.status_code.help_text')
    )
    page_title = models.CharField(
        max_length=255, blank=True, null=True, editable=False,
        verbose_name=_('Link.page_title.verbose_name'),
        help_text=_('Link.page_title.help_text')
    )

    position = models.PositiveSmallIntegerField(
        # Note: Will be set in admin via adminsortable2
        # The JavaScript which performs the sorting is 1-indexed !
        default=0, blank=False, null=False
    )

    def update_response_info(self):
        try:
            r = requests.get(url=self.url, allow_redirects=True, timeout=10)
        except HTTPError as err:
            logger.exception(f'Error get {self.url!r}', err)
            self.status_code = None
            self.page_title = None
            return

        logger.debug('%r: %r', self.url, r.headers)

        self.last_check = timezone.now()
        self.status_code = r.status_code

        if r.status_code == 200:
            titles = re.findall(r'<title>(.+?)</title>', r.text)
            if not titles:
                logger.warning(f'No title found in {self.url!r}')
            else:
                title = titles[0]
                logger.info('Found title: %r', title)

                self.page_title = striptags(title)  # TODO: remove with a better clean method!
                if not self.name:
                    logger.debug('set name to: %r', self.page_title)
                    self.name = self.page_title

    def full_clean(self, **kwargs):
        if self.url is not None:
            self.update_response_info()
        return super().full_clean(**kwargs)

    def __str__(self):
        return self.url

    class Meta:
        abstract = True
