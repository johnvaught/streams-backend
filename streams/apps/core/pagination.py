from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import Response


class LimitOffsetPaginationTime(LimitOffsetPagination):
    def get_paginated_response(self, data, time):
        return Response({
            'count': self.count,
            'time': time,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
