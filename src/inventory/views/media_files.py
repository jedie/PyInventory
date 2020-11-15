import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic.base import View
from django.views.static import serve

from inventory.models import ItemImageModel


logger = logging.getLogger(__name__)


class UserMediaView(View):
    """
    Serve MEDIA_URL files, but check the current user:
    """

    def get(self, request, user_id, path):
        media_path = f'user_{user_id}/{path}'

        if not request.user.is_superuser:
            if request.user.id != user_id:
                # A user tries to access a file from a other use?
                if request.user.id is None:
                    logger.error(f'Anonymous try to access files from: {user_id!r}')
                else:
                    logger.error(f'Wrong user ID: {request.user.id!r} is not {user_id!r}')
                raise PermissionDenied

            # Check if the image really exists:
            qs = ItemImageModel.objects.filter(
                user_id=request.user.id,
                image=media_path
            )
            if not qs.exists():
                raise Http404(_('Image "%(path)s" does not exist') % {'path': media_path})

        # Send the file to the user:
        return serve(
            request,
            path=media_path,
            document_root=settings.MEDIA_ROOT,
            show_indexes=False
        )
