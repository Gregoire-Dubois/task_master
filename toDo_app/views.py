from datetime import date
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from toDo_app.permissions import IsOwnerOrReadOnly
from toDo_app.models import Tache, User
from toDo_app.serializers import TacheSerializer, UserSerializer, TaskCheckerSerializer
from rest_framework import mixins, generics, permissions
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
        "Taches terminées": reverse('tasks-finish', request=request, format=format),
        "Visualisation des taches sur un jour": reverse('tasks-visualisator', request=request, format=format)

    })

#################################################################################################

# display of task list
class TacheList(LoginRequiredMixin, mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView,):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Tache.objects.filter(finishTask=False)
    serializer_class = TacheSerializer

    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    # oblige to be autentificated for create task


    def get_queryset(self):
        user = self.request.user
        return Tache.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        finishTask = self.request.GET.get('finishTask')
        if finishTask!=True:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#################################################################################################
# il reste encore a bloquer l'accès à la liste des users

# List of task finished
class TacheFinishList(LoginRequiredMixin, mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    serializer_class = TacheSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    #display only task's user
    def get_queryset(self):
        user = self.request.user
        return Tache.objects.filter(owner=user).filter(finishTask=True)

    # oblige to be autentificated for creat task

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################

# display details of one task finish

class TacheFinishDetail(LoginRequiredMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    # restriction for read only task if is identificate and not the owner
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#################################################################################################

# display details of one task

class TacheDetail(LoginRequiredMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'
    
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

class UsersList(LoginRequiredMixin, mixins.ListModelMixin,
                generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################

# display list and number tasks on D day

"""
Créer une view qui : 
- retourne la liste des taches enrgistrées sur 1 jour J
- retourne le nombre de taches dans la liste sur le jour J 
- permet de modifier le jour J 
"""

class TasksVisulisator(LoginRequiredMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskCheckerSerializer
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    #display only task's user
    def get_queryset(self):
        user = self.request.user
        return Tache.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#################################################################################################

# display details of one user

class UserDetails(LoginRequiredMixin, mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#################################################################################################

# display all tasks for this day

class TacheForTodayList(LoginRequiredMixin, mixins.ListModelMixin,
                  generics.GenericAPIView):

    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    epoch = '1970-1-1'

    #queryset = Tache.objects.all().filter(checkDate__range=[epoch, date.today()]).filter(finishTask=False)
    serializer_class = TacheSerializer

    # oblige to be autentificated for create task
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #display only task's user
    def get_queryset(self):
        epoch = '1970-1-1'
        user = self.request.user
        return Tache.objects.filter(owner=user).filter(checkDate__range=[epoch, date.today()]).filter(finishTask=False)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#################################################################################################

# display details of one task for today

class TacheForTodayDetail(LoginRequiredMixin, mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin, 
                            mixins.DestroyModelMixin, 
                            generics.GenericAPIView):

    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    login_url = '/api-auth/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)