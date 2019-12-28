from django.db import models
from django_enumfield import enum
from django_enumfield.db.fields import EnumField
from model_utils.models import TimeStampedModel


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
    regular_member_minimum_week = models.SmallIntegerField(
        default=3,
        blank=True,
        null=False,
        verbose_name="정회원 최소 근속 주수",
        help_text="설정한 주 동안은 운동을 채우지 못해도 정회원으로 남습니다.",
    )

    objects = MetaManager()
