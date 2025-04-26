from django.db import models
from projects.models import Project
from users.models import CustomUser
from django.utils import timezone
from datetime import timedelta


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def total_tracked_time(self):
        from django.utils.timezone import now
        total = timedelta()
        for timer in self.timers.all():
            end = timer.end_time or now()
            total += end - timer.start_time
        return total

    @property
    def get_total_time_display(self):
        total = self.total_tracked_time
        total_seconds = int(total.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}h{minutes:02}m{seconds:02}s"

    def get_user_times(self):
        from django.utils.timezone import now
        from collections import defaultdict
        from datetime import timedelta

        user_totals = defaultdict(timedelta)

        for timer in self.timers.select_related('user'):
            user = timer.user
            if user:
                end_time = timer.end_time or now()
                user_totals[user] += end_time - timer.start_time

        return user_totals.items()


class TaskTimer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)  # אם טרם הסתיים

    def is_active(self):
        return self.end_time is None

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time

    def __str__(self):
        return f"{self.task} | {self.user} | {self.start_time} - {self.end_time or 'Running'}"