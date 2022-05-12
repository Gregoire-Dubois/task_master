from toDo_app.models import Tache
from rest_framework import serializers
from django.contrib.auth.models import User


#################################################################################################

class TacheSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Tache
        fields = ['id','owner','number','taskResume','creationDate','checkDate','finishTask']

#################################################################################################

class TaskBydaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['id','owner','number', 'taskResume','creationDate','checkDate','finishTask']

#################################################################################################

class UserSerializer(serializers.ModelSerializer):
    taches = serializers.PrimaryKeyRelatedField(many=True, queryset=Tache.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'taches']

#################################################################################################


"""
class TacheSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.CharField(required=False, allow_blank=False,)
    taskResume = serializers.CharField()
    creationDate = serializers.DateField()
    checkDate = serializers.DateField()
    finishTask = serializers.BooleanField()

    def create(self, validated_data):
        
        #Create and return a new `Tache` instance, given the validated data.
        
        return Tache.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
       #Update and return an existing `Tache` instance, given the validated data.
        
        instance.number = validated_data.get('number', instance.number)
        instance.taskResume = validated_data.get('taskResume', instance.taskResume)
        instance.creationDate = validated_data.get('creationDate', instance.creationDate)
        instance.checkDate = validated_data.get('checkDate', instance.checkDate)
        instance.finishTask = validated_data.get('finishTask', instance.finishTask)
        instance.save()
        return instance

"""

#################################################################################################

"""
    
class TaskBydaySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tache
        fields=['url', 'id','owner','number', 'taskResume','creationDate','checkDate','finishTask']

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']

"""