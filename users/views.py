from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from .models import Course, Student
from django.db.models import Value, Count, CharField


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.user.is_superuser:
        return render(request,"users/admin_index.html",{
            "courses": Course.objects.all()
        })
    return render(request, "users/index.html", {

    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })

def enroll_view(request):
    # Make sure that user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    courses_avalible_seats = []
    not_enroll_courses_avalible_seats = [0]

    user_courses = Student.objects.get(pk=(request.user.id-1)).courses.all()
    non_user_courses = Course.objects.exclude(id__in=Student.objects.get(pk=(request.user.id-1)).courses.all())

    for course in Course.objects.all():
        courses_avalible_seats.append(course.max_seats-course.courses.all().count())

    for course in non_user_courses:
        not_enroll_courses_avalible_seats.append(course.max_seats-course.courses.all().count())

    return render(request, "users/enroll.html", {
        "all_courses": Course.objects.all(),
        "user_courses": user_courses,
        "non_user_courses": non_user_courses,
        "avalible_seats": courses_avalible_seats,
        "not_enroll_avalible_seats": not_enroll_courses_avalible_seats
    })

def course_info(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course not found.")

    return render(request, "users/course.html", {
        "course": course,
    })

def admin_course_info(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course not found.")

    # Make sure that admin is logged in
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "users/admin_course.html", {
        "course": course,
        "students": Course.objects.get(pk=course_id).courses.all(),
        "avalible_seats": (course.max_seats-course.courses.all().count()),
    })

def enroll_course(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(pk=course_id)
        student = Student.objects.get(pk=(request.user.id-1))
        student.courses.add(course)
    return HttpResponseRedirect(reverse("enroll"))

def unenroll_course(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(pk=course_id)
        student = Student.objects.get(pk=(request.user.id-1))
        student.courses.remove(course)
    return HttpResponseRedirect(reverse("enroll"))


#Course.objects.get(pk=1).courses.all().count() #reverse ManyToMany