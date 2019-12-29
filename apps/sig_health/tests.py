from apps.sig_health.models import Member, Meta, Workout, WorkoutAdmit, WorkoutCheer
from apps.slack_outbound.models import MessageTask, ReplyTask
from django.test import TestCase
from model_bakery import baker


class WorkoutAdmitTests(TestCase):
    def setUp(self):
        self.meta = baker.make(Meta)
        person_list = baker.prepare(Member, _quantity=10)
        Member.objects.bulk_create(person_list)
        self.person_list = list(Member.objects.all())

    def test_admit_create(self):
        member = self.person_list[0]
        thread_ts = "1234.1234"
        for admitted_by in self.person_list[
            1 : (self.meta.minimum_admit_emoji_num + 1)
        ]:
            WorkoutAdmit.objects.create(
                admitted_by=admitted_by, member=member, thread_ts=thread_ts
            )
        self.assertTrue(
            Workout.objects.filter(thread_ts=thread_ts, member=member).exists()
        )

    def test_do_not_allow_self_admit(self):
        with self.assertRaises(BaseException):
            admit = WorkoutAdmit(
                admitted_by=self.person_list[0],
                member=self.person_list[0],
                thread_ts="1234.1234",
            )
            admit.full_clean()

    def test_do_allow_supermember_self_admit(self):
        member = baker.make(Member, is_superuser=True)
        admit = WorkoutAdmit(admitted_by=member, member=member, thread_ts="1234.1234")
        admit.full_clean()

    def test_admit_twice(self):
        thread_ts = "1234.1234"
        with self.assertRaises(BaseException):
            WorkoutAdmit.objects.create(
                thread_ts=thread_ts,
                admitted_by=self.person_list[1],
                member=self.person_list[0],
            )
            WorkoutAdmit.objects.create(
                thread_ts=thread_ts,
                admitted_by=self.person_list[1],
                member=self.person_list[0],
            )


class WorkoutTests(TestCase):
    def setUp(self):
        member_list = baker.prepare(Member, _quantity=10)
        Member.objects.bulk_create(member_list)
        cheer_list = []
        for index in range(1, 8):
            cheer_list += baker.prepare(WorkoutCheer, week_count=index, _quantity=5)
        WorkoutCheer.objects.bulk_create(cheer_list)

    def test_cheer_on_workout(self):
        member = Member.objects.first()
        workout = baker.make(Workout, member=member)
        self.assertTrue(
            ReplyTask.objects.filter(
                thread_ts=workout.thread_ts, text__startswith=f"<@{member.slack_id}>"
            ).exists()
        )

    def test_cheer_on_workout_multiple(self):
        member = Member.objects.first()
        baker.make(Workout, member=member)
        baker.make(Workout, member=member)
        baker.make(Workout, member=member)
        self.assertGreaterEqual(
            ReplyTask.objects.filter(text__startswith=f"<@{member.slack_id}>").count(),
            3,
        )

    def test_cheer_on_workout_explode(self):
        member = Member.objects.first()
        baker.make(Workout, member=member, _quantity=10)
        self.assertGreaterEqual(
            ReplyTask.objects.filter(text__startswith=f"<@{member.slack_id}>").count(),
            7,
        )


class MemberTests(TestCase):
    def setUp(self):
        self.me = Member.objects.create(slack_id="UCL25JV2R")

    def test_message_task(self):
        self.me.is_regular = True
        self.me.save(update_fields=["is_regular"])
        self.assertEqual(MessageTask.objects.count(), 1)
