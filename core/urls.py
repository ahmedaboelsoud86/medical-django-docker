from django.urls import path # type: ignore
from . import views

urlpatterns = [
   path('', views.index,name='index'),
   path('create_post', views.CreatePost,name='create_post'),
   path('update_post/<int:pk>/', views.updatepost,name='update_post'),
   path('delete_post/<int:pk>/', views.deletepost,name='delete_post'),
   #path('test-permission', views.permission,name='permission'),
   path('test-permission', views.permission,name='test-permission'),

   path('users/groups', views.groups,name='groups'),
   path('users/create/group', views.createGroup,name='create_group'),
   path('delete/group/<int:pk>/', views.deletegroup,name='delete_group'),
   path('users/update/group/<int:pk>/', views.updateGroup,name='update_group'),

   # path('users/permissions', views.permissions,name='permissions'),
   # path('users/create/permission', views.createPermission,name='create_permission'),
   # path('delete/permission/<int:pk>/', views.deletePermission,name='delete_permission'),
   # path('users/update/permission/<int:pk>/', views.updatePermission,name='update_permission'),
]  