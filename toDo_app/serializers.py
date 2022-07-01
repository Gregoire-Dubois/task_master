from toDo_app.models import Tache
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User

#################################################################################################
# serializer for list task not finish
class TacheSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='tasks-list')

    class Meta:
        model = Tache
        fields = ['id','url','owner','number','taskResume',
                  'creationDate','checkDate','finishTask']

    # create task is only for futur, but if user finish task a time befor today it's possible to close task
    def validate(self, data):
        if data['checkDate'] < date.today() and data['finishTask']==False:
            raise serializers.ValidationError("La relance ne peut être antérieure à aujourd'hui")
        return data


#################################################################################################
# serializer for list users
class UserSerializer(serializers.ModelSerializer):
    taches = serializers.PrimaryKeyRelatedField(many=True, queryset=Tache.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'taches']

#################################################################################################
# serializer for list tasks for today an task delayed
class TaskBydaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']

    def validate(self, data):
        if data['checkDate'] < date.today() and data['finishTask']==False:
            raise serializers.ValidationError("La relance ne peut être antérieure à aujourd'hui")
        return data



#################################################################################################

# serializer for check task in one day

class TaskCheckerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']
