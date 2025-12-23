from typing import Any

from django.core.cache import cache
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Project


@receiver(m2m_changed, sender=Project.users.through)
def invalidate_user_projects_cache(
    sender, instance, action: str, pk_set: set[int], **kwargs: Any
) -> None:
    print("Сигнал 'invalidate_user_projects_cache' викликаний")
    if action not in {"post_add", "post_remove", "post_clear"}:
        return

    for user_id in pk_set or []:
        cache_key = f"user:{user_id}:project"
        cache.delete(cache_key)
