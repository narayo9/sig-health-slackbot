from apps.slack_outbound.models import ReplyTask
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from django_enumfield import enum
from django_enumfield.db.fields import EnumField
from model_utils.models import TimeStampedModel

from django_project.utils import get_week_start_end


class UniqueRowIDEnum(enum.Enum):
    zero = 0

    __default__ = zero


class MetaManager(models.Manager):
    def get_main(self):
        return self.get_queryset().get(id=UniqueRowIDEnum.zero)


class Meta(TimeStampedModel):
    id = EnumField(UniqueRowIDEnum, primary_key=True)
    channel_id = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="#sig-헬스 채널 ID"
    )
    oauth_access_token = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="botuser oauth token"
    )
    admit_emoji = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name="운동 인정 이모지",
        default="kr_admit",
    )
    regular_member_emoji = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="정회원 이모지", default="star2"
    )
    minimum_admit_emoji_num = models.SmallIntegerField(
        default=1,
        blank=True,
        null=False,
        verbose_name="최소 인정 이모지 횟수",
        help_text="이 횟수 이상 유저에게 이모지가 찍혀야 운동으로 인정됩니다.",
    )
    minimum_regular_member_workout_num = models.SmallIntegerField(
        default=4,
        blank=True,
        null=False,
        verbose_name="정회원 최소 주별 운동 수",
        help_text="일주일에 이 이상 운동하면 정회원으로 등극합니다.",
    )
    hard_mode_minimum_regular_member_workout_num = models.SmallIntegerField(
        default=5,
        blank=True,
        null=False,
        verbose_name="하드모드 정회원 최소 주별 운동 수",
        help_text="하드모드 정회원은 일주일에 이 이상 운동하면 정회원으로 등극합니다.",
    )

    objects = MetaManager()


class UnregularMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_regular=False)

    def set_regular(self):
        start_date, end_date = get_week_start_end()
        meta = Meta.objects.get_main()
        self.get_queryset().annotate(
            this_week_workout_count=Count(
                "workout_set",
                filter=Q(created__date__gte=start_date, created__date__lte=end_date),
            )
        ).filter(
            this_week_workout_count__gte=meta.minimum_regular_member_workout_num
        ).update(
            is_regular=True
        )


class RegularMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_regular=True)


class Member(TimeStampedModel):
    slack_id = models.CharField(max_length=100, primary_key=True)
    is_superuser = models.BooleanField(default=False)
    is_regular = models.BooleanField(default=False)
    is_hard_mode = models.BooleanField(default=False, help_text="자체 하드 모드 여부")

    objects = models.Manager()

    regular_members = RegularMemberManager()
    unregular_members = UnregularMemberManager()

    def is_regular_on_week(self, weekdelta: int = 0) -> bool:
        start_date, end_date = get_week_start_end(weekdelta)
        meta = Meta.objects.get_main()
        return (
            self.is_regular
            or self.workout_set.filter(
                created__date__gte=start_date, created__date__lte=end_date
            ).count()
            >= meta.minimum_regular_member_workout_num
        )

    def get_tag_text(self):
        return f"<@{self.slack_id}>"

    def set_regular(self, commit=True):
        if not self.is_regular and self.is_regular_on_week():
            self.is_regular = True
            if commit:
                self.save()

    def get_regulared_text(self):
        return f"{self.get_tag_text()} 님, 정회원이 되신 걸 축하드려요!! :party-blob: :musclegrowth_rainbow:"  # noqa: B950


class WorkoutManager(models.Manager):
    def get_current_week_workout_count(self, member: Member) -> int:
        start_date, end_date = get_week_start_end()
        return Workout.objects.filter(
            created__date__gte=start_date, created__date__lte=end_date, member=member
        ).count()


class Workout(TimeStampedModel):
    thread_ts = models.CharField(max_length=100, primary_key=True)
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="workout_set",
        null=False,
        blank=False,
    )
    objects = WorkoutManager()


class WorkoutAdmit(TimeStampedModel):
    admitted_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="admit_set",
        null=False,
        blank=False,
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="admitted_set",
        null=False,
        blank=False,
    )
    thread_ts = models.CharField(max_length=100)

    def clean(self):
        if not self.pk:
            if self.admitted_by == self.member and not self.member.is_superuser:
                raise ValidationError("자기 자신의 운동을 인정할 수 없습니다.")

    class Meta:
        unique_together = (("thread_ts", "admitted_by"),)


class WorkoutCheer(TimeStampedModel):
    week_count = models.SmallIntegerField(
        validators=[MaxValueValidator(7), MinValueValidator(1)]
    )
    text = models.TextField(null=False, blank=False)

    def create_reply_task(self, thread_ts: str, member: Member, execute_at=None):
        return ReplyTask.objects.create(
            thread_ts=thread_ts,
            text=f"{member.get_tag_text()} 님, {self.text}",
            execute_at=execute_at or timezone.now(),
        )
