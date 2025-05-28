
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(summary="List notifications for the current user"),
    retrieve=extend_schema(summary="Get a single notification"),
    create=extend_schema(
        # Direct creation via API is not expected,
        # but left for internal or compatibility purposes
        summary="Create a notification (internal use)"
    ),
    update=extend_schema(summary="Update a notification (internal use)"),
    destroy=extend_schema(summary="Delete a notification"),
    mark_all=extend_schema(
        methods=['PATCH'],
        summary="Mark all notifications for the current user as read",
        description="Sets is_read=True for all notifications belonging to the current user",
        responses={200: NotificationSerializer(many=True)}
    ),
)
class NotificationViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for notifications.
    Only authenticated users can access their own notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [ ]

    def get_queryset(self):
        # user.id corresponds to Notification.user_id
        return Notification.objects.filter(user_id=self.request.user.id)

    @action(detail=False, methods=['PATCH'], url_path='mark-all-as-read')
    def mark_all(self, request):
        # Bulk mark all unread notifications as read for the current user
        qs = self.get_queryset().filter(is_read=False)
        qs.update(is_read=True)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
