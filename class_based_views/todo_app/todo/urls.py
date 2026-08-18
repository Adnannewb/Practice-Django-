from django.urls import path
from .views import TaskListView,TaskCreateView,TaskDetailView,TaskUpdateView,TaskDeleteView,get_session,set_session,delete_session,set_cookie,get_cookie,delete_cookie
urlpatterns = [
    path("",TaskListView.as_view(),name="home"),
    path("detail/<int:pk>/",TaskDetailView.as_view(),name="taskdetail"),
    path("add_task/",TaskCreateView.as_view(),name="taskcreate"),
    path("update/<int:pk>/",TaskUpdateView.as_view(),name="taskupdate"),
    path("delete/<int:pk>/",TaskDeleteView.as_view(),name="taskdelete"),
    path("set-session/",set_session,name='set-session'),
    path("get-session/",get_session,name='get-session'),
    path("delete-session/",delete_session,name='delete-session'),
    path("set-cookie/",set_cookie,name='set-cookie'),
    path("get-cookie/",get_cookie,name='get-cookie'),
    path("delete-cookie/",delete_cookie,name='delete-cookie'),
]
