from rest_framework import generics, status
from rest_framework.response import Response
from .models import Mess, MembershipRequest
from mess.serializers import MembershipRequestSerializer, MessSerializer,MembershipSendSerializer
from .permissions import IsManager
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsAuthenticatedAndUser

# ---------------------- Mess Management Views ---------------------- #
class CreateMessAPIView(generics.CreateAPIView):
    """
    View to allow managers to create a new mess.
    """
    serializer_class = MessSerializer
    permission_classes = [IsManager]

    def perform_create(self, serializer):
        # Assign logged-in user as the manager for the new mess
        serializer.save(manager=self.request.user)


class MessListAPIView(generics.ListAPIView):
    """
    View to list all messes available.
    """
    queryset = Mess.objects.all()
    serializer_class = MessSerializer
    permission_classes = [IsAuthenticated]


# ---------------- Membership Request Logic ----------------
# Send a membership request
class SendMembershipRequestView(generics.CreateAPIView):
    """
    Allows a user to send a request to join a specific mess.
    """
    serializer_class = MembershipSendSerializer
    permission_classes = [IsAuthenticatedAndUser]

    def perform_create(self, serializer):
        # Prevent duplicates: check if a pending request already exists
        if MembershipRequest.objects.filter(
            user=self.request.user,
            mess=serializer.validated_data['mess'],
            status='pending'
        ).exists():
            return Response({"error": "You already have a pending request for this mess."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=self.request.user)


# List pending membership requests for a manager's mess
class ManagerMembershipRequestsView(generics.ListAPIView):
    """
    Allows a manager to view all pending membership requests for their mess.
    """
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        # Filter membership requests for messes managed by the current manager
        return MembershipRequest.objects.filter(mess__manager=self.request.user, status='pending')


# class ApproveRejectMembershipRequestView(generics.GenericAPIView):
#     """
#     Allows managers to view membership request details and approve/reject a membership request.
#     GET request to view request status.
#     PUT request to approve/reject a membership request.
#     """
#     serializer_class = MembershipRequestSerializer
#     permission_classes = [IsManager]

#     def get_queryset(self):
#         """Filters only membership requests pending for the manager's mess."""
#         return MembershipRequest.objects.filter(mess__manager=self.request.user, status='pending')

#     # Handle GET to show the membership request details with the status options
#     def get(self, request, *args, **kwargs):
#         """
#         Fetch the membership request details and available status choices.
#         """
#         membership_request = MembershipRequest.objects.get(pk=kwargs['pk'])  # Find specific request
#         if not membership_request.mess.manager == request.user:
#             return Response({"error": "You are not authorized for this request."}, status=status.HTTP_403_FORBIDDEN)

#         # Return available status options for frontend select/dropdown population
#         return Response(
#             {
#                 "mess_name": membership_request.mess.name,
#                 "current_status": membership_request.status,
#                 "status_choices": ["approved", "rejected"]
#             },
#             status=status.HTTP_200_OK
#         )

#     # Handle PUT to approve/reject membership requests
#     def put(self, request, *args, **kwargs):
#         """
#         Handles the actual approve/reject operation logic.
#         """
#         membership_request = MembershipRequest.objects.get(pk=kwargs['pk'])  # Find specific request
#         if not membership_request.mess.manager == request.user:
#             return Response({"error": "You are not authorized for this request."}, status=status.HTTP_403_FORBIDDEN)

#         # Extract the action
#         action = request.data.get('status')

#         # Validate the action
#         if action not in ['approved', 'rejected']:
#             return Response({"error": "Invalid status. Must be 'approved' or 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

#         # Update and save
#         membership_request.status = action
#         membership_request.save()

#         # Return success message
#         return Response(
#             {
#                 "message": f"Membership request '{action}' successfully.",
#                 "mess_name": membership_request.mess.name,
#                 "status": membership_request.status,
#             },
#             status=status.HTTP_200_OK
#         )



class ApproveRejectMembershipRequestView(generics.GenericAPIView):
    """
    Handle the logic for approving or rejecting a membership request.
    """
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        """
        Fetch a specific membership request to show details and options.
        """
        try:
            membership_request = MembershipRequest.objects.get(pk=kwargs['pk'])
            if membership_request.mess.manager != request.user:
                return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

            return Response({
                "mess_name": membership_request.mess.name,
                "user": membership_request.user.username,
                "current_status": membership_request.status,
                "status_choices": ["approved", "rejected"]
            }, status=status.HTTP_200_OK)
        except MembershipRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        Handle approve/reject action.
        """
        try:
            membership_request = MembershipRequest.objects.get(pk=kwargs['pk'])
            if membership_request.mess.manager != request.user:
                return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

            action = request.data.get('status')
            if action not in ['approved', 'rejected']:
                return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

            membership_request.status = action
            membership_request.save()

            if action == 'approved':
                # Handle logic for approved members (e.g., add them as members of the mess)
                # This part depends on how you handle memberships in your system.
                pass

            return Response({
                "message": f"Request {action} successfully.",
                "status": membership_request.status
            }, status=status.HTTP_200_OK)

        except MembershipRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
        

from rest_framework.views import APIView
class MessMembersListView(APIView):
    """
    View to list all approved members of a specific mess managed by the logged-in manager.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Fetch the mess by its ID
            mess = Mess.objects.get(pk=pk, manager=request.user)

            # Fetch approved membership requests for this mess
            approved_requests = MembershipRequest.objects.filter(mess=mess, status='approved')

            # Create the response data
            members_data = [
                {
                    "member_name": request.user.username,
                    "email": request.user.email,
                }
                for request in approved_requests
            ]

            return Response({
                "mess_name": mess.name,
                "location": mess.location,
                "members": members_data
            }, status=200)

        except Mess.DoesNotExist:
            return Response({"error": "Mess not found or you are not the manager of this mess."}, status=404)