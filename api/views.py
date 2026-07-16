from rest_framework import viewsets
from app.models import *
from .serializer import *

# Create your views here.

class AccountViewAPI(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
