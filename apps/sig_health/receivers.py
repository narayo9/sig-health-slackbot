import random

from apps.sig_health.models import Member, Meta, Workout, WorkoutAdmit, WorkoutCheer
from apps.slack_outbound.models import MessageTask
from django.db.models.signals import post_save, pre_save
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


@receiver(post_save, sender=Workout)
def set_regular_workout_created(instance: Workout, created, **kwargs):
    if created:
        if (
            not instance.member.is_regular
            and instance.member.has_passed_minimum_on_week()
        ):
            instance.member.is_regular = True
            instance.member.save()


@receiver(pre_save, sender=Member)
def set_regulared_member_create_message_task(instance: Member, update_fields, **kwargs):
    try:
        old_instance = Member.objects.get(pk=instance.pk)
    except Member.DoesNotExist:
        pass
    else:
        if not old_instance.is_regular and instance.is_regular:
            MessageTask.objects.create(text=instance.get_regulared_text())


@receiver(pre_save, sender=Member)
def set_unregulared_member_create_message_task(
    instance: Member, update_fields, **kwargs
):
    try:
        old_instance = Member.objects.get(pk=instance.pk)
    except Member.DoesNotExist:
        pass
    else:
        if old_instance.is_regular and not instance.is_regular:
            MessageTask.objects.create(text=instance.get_unregulared_text())
