from . import views
from django.urls import path

app_name = 'Courses'

urlpatterns = [
    path('', views.courses,name='courses'),
    path('<slug:course_name>/topics/', views.CourseTopicsView.as_view(), name='topics'), 
    path('<slug:course_name>/topic/<int:lab_no>/', views.topicdetails, name='topic_details'),
    path('<slug:course_name>/labs/<int:lab_no>/', views.LabDetailsView.as_view(), name='labs')
    ]