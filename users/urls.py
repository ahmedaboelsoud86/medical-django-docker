from django.urls import path 
from . import views

urlpatterns = [
   path('', views.index,name='users'),
   path('create_user', views.CreateUser,name='create_user'),
   path('update_user/<int:pk>/', views.updateUser,name='update_user'),
   path('delete_user/<int:pk>/', views.deleteUser,name='delete_user'),
   path('delete_all_user', views.deleteAllUser,name='deleteallusers'),
   path('user_permissions/<int:pk>/', views.userPermissions,name='user_permissions'),
   path('clear_user_group/<int:pk>/', views.clearUserGroup,name='clear_user_group'),
   path('clear_user_permissions/<int:pk>/', views.clearUserPermissions,name='clear_user_permissions'),
   path('sign-up', views.signUp,name='sign_up'),
   #path('employees', views.employees,name='employees'),
   path('monthly_salaries/<int:pk>/', views.monthlySalaries,name='monthly_salaries'),
   path('deductions_incentives', views.deductionsIncentives,name='deductions_incentives'),
   path('add_deductions_incentives', views.addDeductionsIncentives,name='add_deductions_incentives'),
]