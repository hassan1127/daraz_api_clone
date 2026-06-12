from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    UserRegistrationSerializer,
    AdminRegistrationSerializer,
    UserProfileSerializer,
    SellerRequestActionSerializer,
)
from .permissions import IsAdmin

User = get_user_model()


# ── REGISTRATION ───────────────────────────────────────

class UserRegisterView(generics.CreateAPIView):
    """Anyone can register as a normal user."""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class AdminRegisterView(generics.CreateAPIView):
    """Only an existing admin can create another admin."""
    serializer_class = AdminRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# ── PROFILE ────────────────────────────────────────────

class MeView(generics.RetrieveAPIView):
    """Returns the logged-in user's own profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ── SELLER REQUEST (user side) ─────────────────────────

class SellerRequestView(views.APIView):
    """Logged-in USER submits a request to become a seller."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != 'USER':
            return Response(
                {'detail': 'Only regular users can request seller status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.seller_request_status == 'PENDING':
            return Response(
                {'detail': 'You already have a pending request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.seller_request_status == 'APPROVED':
            return Response(
                {'detail': 'You are already a seller.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.seller_request_status = 'PENDING'
        user.save()
        return Response({'detail': 'Seller request submitted. Awaiting admin approval.'})


# ── ADMIN PANEL ────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    """Admin sees all users."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = User.objects.all()


class PendingSellerRequestsView(generics.ListAPIView):
    """Admin sees all pending seller requests."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.filter(seller_request_status='PENDING')


class SellerRequestActionView(views.APIView):
    """
    Admin approves or rejects a seller request.
    Body: { "action": "approve" } or { "action": "reject" }
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        serializer = SellerRequestActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_user = get_object_or_404(User, id=user_id, seller_request_status='PENDING')
        action = serializer.validated_data['action']

        if action == 'approve':
            target_user.role = 'SELLER'
            target_user.seller_request_status = 'APPROVED'
            target_user.save()
            return Response({'detail': f'{target_user.email} is now a seller.'})

        elif action == 'reject':
            target_user.seller_request_status = 'REJECTED'
            target_user.save()
            return Response({'detail': f'{target_user.email} seller request rejected.'})