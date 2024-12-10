from django.urls import path
from .views import CreateMessAPIView,MessListAPIView,SendMembershipRequestView,ManagerMembershipRequestsView,ApproveRejectMembershipRequestView,MessMembersListView


urlpatterns = [
    path('create/', CreateMessAPIView.as_view(), name='create-mess'),
    path('list/', MessListAPIView.as_view(), name='mess-list'),
    path('membership/send/', SendMembershipRequestView.as_view(), name="send-membership-request"),
    path('manager/request/', ManagerMembershipRequestsView.as_view(), name="manager-membership-requests"),
    path('manager/request/<int:pk>/', ApproveRejectMembershipRequestView.as_view(), name="approve-reject-request"),
    path('mess/<int:pk>/members/', MessMembersListView.as_view(), name='mess-members'),
]
