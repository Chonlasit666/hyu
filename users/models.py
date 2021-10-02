from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=5)
    course_name = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    academic_year = models.PositiveIntegerField()
    max_seats = models.PositiveIntegerField()
    avalibility = models.BooleanField()

    def __str__(self):
        return f"({self.course_id}): {self.course_name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True, related_name="courses")

    def __str__(self):
        return f"({self.id}) {self.user.first_name} {self.user.last_name}"
