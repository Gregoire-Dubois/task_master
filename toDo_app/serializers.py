from toDo_app.models import Tache
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User

#################################################################################################

class TacheSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    # create only task for futur
    #checkDate = serializers.DateField(validators=[validate_checkDate])
    # Finish task

    class Meta:
        model = Tache
        fields = ['id','owner','number','taskResume','creationDate','checkDate','finishTask']

    def validate(self, data):
        if data['checkDate'] < date.today() and data['finishTask']==False:
            raise serializers.ValidationError("La relance ne peut être antérieure à aujourd'ui")
        return data
#################################################################################################

class TaskBydaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']

    def validate(self, data):
        if data['checkDate'] < date.today() and data['finishTask']==False:
            raise serializers.ValidationError("La relance ne peut être antérieure à aujourd'ui")
        return data

#################################################################################################

class UserSerializer(serializers.ModelSerializer):
    taches = serializers.PrimaryKeyRelatedField(many=True, queryset=Tache.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'taches']

#################################################################################################
