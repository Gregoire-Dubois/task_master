from datetime import date, datetime
from django.core.exceptions import ValidationError
from toDo_app.permissions import IsOwnerOrReadOnly
from toDo_app.models import Tache, User
from toDo_app.serializers import TacheSerializer, UserSerializer, TaskBydaySerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


#################################################################################################

# creation of link in the first web page
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "liste des utilisateurs": reverse('users-list', request=request, format=format),
        "Liste des taches": reverse('tasks-list', request=request, format=format),
        "Taches à faire aujourd'hui": reverse('tasks-today', request=request, format=format),
        "Taches terminées": reverse('tasks-finish', request=request, format=format)
    })

#################################################################################################

# display of task list
class TacheList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Tache.objects.filter(finishTask=False)
    serializer_class = TacheSerializer

    # oblige to be autentificated for creat task
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        finishTask = self.request.GET.get('finishTask')
        if finishTask!=True:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#################################################################################################
# List of task finished
class TacheFinishList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Tache.objects.filter(finishTask=True)
    serializer_class = TacheSerializer

    # oblige to be autentificated for creat task
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################
# display details of one task finish

class TacheFinishDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

    # restriction for read only task if is identificate and not the owner
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#################################################################################################
# display details of one task

class TacheDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    
    #restriction for read only task if is identificate and not the owner
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#################################################################################################
# display list of User

class UsersList(mixins.ListModelMixin,
                generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################
# display details of one user

class UserDetails(mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#################################################################################################

# display all tasks for this day

class TacheForTodayList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    
    epoch = '1970-1-1'

    queryset = Tache.objects.all().filter(checkDate__range=[epoch, date.today()]).filter(finishTask=False)
    serializer_class = TacheSerializer

    # oblige to be autentificated for creat task
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################

# display details of one task for today

class TacheForTodayDetail(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin, 
                            mixins.DestroyModelMixin, 
                            generics.GenericAPIView):

    queryset = Tache.objects.all()

    serializer_class = TacheSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)