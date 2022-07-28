from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

#################################################################################################
# create task is only for futur, but if user finish task a time befor today it's possible to close task

def validate_checkDate(value):
    if value < date.today():
        raise ValidationError("La relance ne peut être antérieur à aujoud'hui")
    return value

#creation class for task
class Tache(models.Model):
    owner = models.ForeignKey('auth.User', related_name='taches', on_delete=models.CASCADE)

    number = models.CharField(max_length=15, blank=False)
    taskResume = models.CharField(max_length=200, blank=False)
    creationDate = models.DateField(auto_now=date.today(), blank=False)
    checkDate = models.DateField(blank=False, null=False, default=date.today(), validators=[validate_checkDate])
    finishTask = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.taskResume

    class Meta:
        ordering = ['checkDate']
#################################################################################################