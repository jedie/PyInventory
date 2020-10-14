"""
    created 28.06.2018 by Jens Diemer <opensource@jensdiemer.de>
    :copyleft: 2018 by the PyInventory team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from django.db.models.signals import post_save, pre_save

# https://github.com/jedie/PyInventory
from inventory.models.discipline import DisciplineModel  # noqa
from inventory.models.distance import DistanceModel  # noqa
from inventory.models.event import CostModel, EventLinkModel, EventModel, ParticipationModel  # noqa
from inventory.models.gpx import GpxModel  # noqa
from inventory.signal_handlers.gpx import gpx_post_save_handler, gpx_pre_save_handler  # noqa


pre_save.connect(receiver=gpx_pre_save_handler, sender=GpxModel)
post_save.connect(receiver=gpx_post_save_handler, sender=GpxModel)
