from apps.sig_health.models import Member, Meta, Workout, WorkoutAdmit, WorkoutCheer
from django.contrib import admin

admin.site.register(Meta)
admin.site.register(Member)
admin.site.register(WorkoutCheer)
admin.site.register(WorkoutAdmit)
admin.site.register(Workout)
