from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('enroll', views.enroll_view, name='enroll'),
    path('<int:course_id>', views.course_info, name="course_info"),
    path('<int:course_id>/enroll_course', views.enroll_course, name="enroll_course"),
    path('<int:course_id>/unenroll_course', views.unenroll_course, name="unenroll_course"),
    path('<int:course_id>/admin_course', views.admin_course_info, name='admin_course'),
    path('admin_index',views.index, name='admin_index' ),
]