import logging 
from django.db import models 
from typing import Any, cast

logger = logging.getLogger('core')

class ReadLoggingQuerySet(models.QuerySet[models.Model]):
    def get(self, *args: Any, **kwargs: Any) -> models.Model:
        obj: models.Model = super().get(*args, **kwargs)
        pk = cast(int | str, obj.pk)
        logger.info("DB read", extra={"model": self.model.__name__, "pk": str(pk)})
        return obj
    
class ReadLoggingManager(models.Manager[models.Model]):
    def get_queryset(self):
        return ReadLoggingQuerySet(self.model, using=self._db)