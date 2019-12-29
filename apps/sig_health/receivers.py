import random

from apps.sig_health.models import Meta, Workout, WorkoutAdmit, WorkoutCheer
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=WorkoutAdmit)
def create_workout_when_admitted(instance, created, **kwargs):
    if created:
        meta = Meta.objects.get_main()
        if (
            WorkoutAdmit.objects.filter(thread_ts=instance.thread_ts).count()
            >= meta.minimum_admit_emoji_num
            and not Workout.objects.filter(thread_ts=instance.thread_ts).exists()
        ):
            Workout.objects.create(thread_ts=instance.thread_ts, member=instance.member)


@receiver(post_save, sender=Workout)
def create_cheer_reply_when_workout_created(instance, created, **kwargs):
    if created:
        try:
            cheer = random.sample(
                list(
                    WorkoutCheer.objects.filter(
                        week_count=Workout.objects.get_current_week_workout_count(
                            instance.member
                        )
                    )
                ),
                1,
            )
            cheer[0].create_reply_task(
                member=instance.member, thread_ts=instance.thread_ts
            )
        except ValueError:
            pass
