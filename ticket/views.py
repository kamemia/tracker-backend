from django.shortcuts import render
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import TicketSerializer
from .models import Ticket

# Create your views here.
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    @action(detail=False, methods=["get"])
    def stats(self, request):
        counts = dict(Ticket.objects.values_list("status").annotate(count=Count("id")).order_by())
        return Response({s: counts.get(s, 0) for s in Ticket.Status.values})