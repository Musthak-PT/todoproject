from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'project'

urlpatterns = [       
    re_path(r'^project/', include([
        path('', login_required(views.ProjectView.as_view()), name='project.index'),
        path('load_projects_datatable', login_required(views.LoadProjectsDatatable.as_view()), name='load.project.datatable'),
        path('create/', login_required(views.ProjectCreateOrUpdateView.as_view()), name='project.create'),
        path('<str:id>/update/', views.ProjectCreateOrUpdateView.as_view(), name='project.update'),
        path('destroy_records/', login_required(views.DestroyProjectRecordsView.as_view()), name='projects.records.destroy'),
        path('active-or-inactive/', login_required(views.ProjectStatusChange.as_view()), name="projects.status_change"),
        path('check-project/', login_required(views.CheckProjectView.as_view()), name='check_project'),
        path('<str:id>/detail-view/', login_required(views.ProjectDetailViewView.as_view()), name='projectdetailed.detail-view'),


    ])),

    re_path(r'^todo/', include([
        path('', login_required(views.TodoView.as_view()), name='todo-view.index'),
        path('load_todo_datatable', login_required(views.LoadTodoDatatable.as_view()), name='load.todo.datatable'),
        path('active/', login_required(views.ActiveInactiveTodo.as_view()), name='active.or.inactive.todo'),
        path('create/', login_required(views.TodoCreateOrUpdateView.as_view()), name='todo.create'),
        path('<str:id>/update/', login_required(views.TodoCreateOrUpdateView.as_view()), name='todo.update'),
        path('destroy_records/', login_required(views.DestroyTodoRecordsView.as_view()), name='todo.records.destroy'),
        path('check-todo/', login_required(views.CheckTodoView.as_view()), name='check_todo'),
])),  

]