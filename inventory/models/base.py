import uuid

from bx_py_utils.models.timetracking import TimetrackingBaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(TimetrackingBaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID')
    )

    class Meta:
        abstract = True
