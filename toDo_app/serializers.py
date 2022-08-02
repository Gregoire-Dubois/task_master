from toDo_app.models import Tache
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User

#################################################################################################
# serializer for list task not finish
class TacheSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields = ['id','owner','number','taskResume','creationDate','checkDate','finishTask']



#################################################################################################
# serializer for list tasks for today an task delayed
class TaskBydaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']


#################################################################################################
# serializer for list users
class UserSerializer(serializers.ModelSerializer):
    taches = serializers.PrimaryKeyRelatedField(many=True, queryset=Tache.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'taches']

#################################################################################################

# serializer for check task in one day

class TaskCheckerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']

#################################################################################################

