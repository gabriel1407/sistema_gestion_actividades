from rest_framework.filters import BaseFilterBackend


class CreatedBetweenFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        if request.GET.get('created__gte', None) is not None:
            queryset = queryset.filter(created__gte=request.GET.get('created__gte'))

        if request.GET.get('created__lte', None) is not None:
            queryset = queryset.filter(created__lte=request.GET.get('created__lte'))

        return queryset