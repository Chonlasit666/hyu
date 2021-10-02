from django.test import Client, TestCase
from .models import Course, Student
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Max

# Create your tests here.
class UserLoginTest(TestCase):

    def setUp(self):
        # Create users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student1',
            first_name='Harry',
            last_name='Potter'
        )

    def test_can_access_login_page(self):
        response = self.client.get(reverse('login'))
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)
        # Make sure that user access to the right page
        self.assertTemplateUsed(response, 'users/login.html')


    def test_index_user(self):
        # Login
        self.client.login(username='student1', password='student1')
        response = self.client.get(reverse('index'))

        # Check our correct user is logged in
        self.assertEqual(str(response.context['user']), 'student1')
        self.assertTemplateUsed(response, 'users/index.html')
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

    def test_index_admin(self):
        # Login to admin account
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('index'))

        # Make sure our correct user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
        # Make sure that admin logged into admin page
        self.assertTemplateUsed(response, 'users/admin_index.html')
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

    def test_index_invalid_user(self):
        # Login with invalid account
        self.client.login(username='notstudent', password='notstudent')
        response = self.client.get(reverse('index'))

        # Make sure that status code is 302
        self.assertEqual(response.status_code, 302)

class UserEnrollTest(TestCase):

    def setUp(self):
        # Create users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student1',
            first_name='Harry',
            last_name='Potter'
        )
        user2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='student2',
            first_name='Alice',
            last_name='Wonderland'
        )

        # Create courses
        Course.objects.create(
            course_id="CN340",
            course_name="Software Engineering",
            semester=1,
            academic_year=2020,
            max_seats=2,
            avalibility=True
        )

        Course.objects.create(
            course_id="CN330",
            course_name="Computer Application Development",
            semester=1,
            academic_year=2020,
            max_seats=3,
            avalibility=True
        )

        # Create students
        Student.objects.create(user=user1)
        Student.objects.create(user=user2)

    def test_enroll_page_not_login(self):

        c1 = Course.objects.get(course_id="CN340")
        s1 = Student.objects.get(pk=1)

        # Enroll course
        s1.courses.add(c1)

        response = self.client.get('/users/enroll')

        # Make sure that status code is 200
        self.assertEqual(response.status_code, 302)


    def test_enroll_page_enroll_course(self):
        # Login
        self.client.login(username='student1', password='student1')

        c2 = Course.objects.get(course_id="CN330")
        s1 = Student.objects.get(pk=1)

        # Enroll course
        s1.courses.add(c2)

        response = self.client.get('/users/enroll')

        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that these values are returned correctly
        self.assertEqual(response.context["all_courses"].count(), 2)
        self.assertEqual(response.context["user_courses"].count(), 1)
        self.assertEqual(response.context['non_user_courses'].count(), 1)
        self.assertEqual(response.context["avalible_seats"], [2, 2])
        self.assertEqual(response.context["not_enroll_avalible_seats"], [0, 2])

    def test_enroll_page_unenroll_course(self):
        # Login
        self.client.login(username='student1', password='student1')

        c1 = Course.objects.get(course_id="CN340")
        s1 = Student.objects.get(pk=1)
        # Add course to student1
        s1.courses.add(c1)

        # Unenroll course
        s1.courses.remove(c1)

        response = self.client.get('/users/enroll')

        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that these values are returned correctly
        self.assertEqual(response.context["all_courses"].count(), 2)
        self.assertEqual(response.context["user_courses"].count(), 0)
        self.assertEqual(response.context['non_user_courses'].count(), 2)
        self.assertEqual(response.context["avalible_seats"], [2, 3])
        self.assertEqual(response.context["not_enroll_avalible_seats"], [0, 2, 3])

    def test_enroll_page_no_course(self):
        # Login
        self.client.login(username='student1', password='student1')
        Course.objects.all().delete()
        s1 = Student.objects.get(pk=1)


        response = self.client.get('/users/enroll')

        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that these values are returned correctly
        self.assertEqual(response.context["all_courses"].count(), 0)
        self.assertEqual(response.context["user_courses"].count(), 0)
        self.assertEqual(response.context['non_user_courses'].count(), 0)
        self.assertEqual(response.context["avalible_seats"], [])
        self.assertEqual(response.context["not_enroll_avalible_seats"], [0])

class UserCourseInfoTest(TestCase):

    def setUp(self):
        # Create user
        user1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student1',
            first_name='Harry',
            last_name='Potter'
        )

        # Create courses
        Course.objects.create(
            course_id="CN340",
            course_name="Software Engineering",
            semester=1,
            academic_year=2020,
            max_seats=2,
            avalibility=True
        )

        Course.objects.create(
            course_id="CN330",
            course_name="Computer Application Development",
            semester=1,
            academic_year=2020,
            max_seats=3,
            avalibility=True
        )

    def test_valid_course_info_login(self):
        # Login
        self.client.login(username='student1', password='student1')

        c1 = Course.objects.get(pk=1)

        response = self.client.get(f'/users/{c1.id}')
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

    def test_valid_course_info_not_login(self):
        # Login
        #self.client.login(username='student1', password='student1')

        c1 = Course.objects.get(pk=1)

        response = self.client.get(f'/users/{c1.id}')
        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

    def test_invalid_course_id(self):
        # Login
        self.client.login(username='student1', password='student1')
        # Check the response of the course that does not exist
        course_max_id = Course.objects.all().aggregate(Max("id"))["id__max"]
        response = self.client.get(f'/users/{course_max_id + 1}')

        # Make sure that status code is 404
        self.assertEqual(response.status_code, 404)


class AdminPageTest(TestCase):
    def setUp(self):
        # Create users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        user1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student1',
            first_name='Harry',
            last_name='Potter'
        )
        user2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='student2',
            first_name='Alice',
            last_name='Wonderland'
        )

        # Create courses
        Course.objects.create(
            course_id="CN340",
            course_name="Software Engineering",
            semester=1,
            academic_year=2020,
            max_seats=2,
            avalibility=True
        )

        Course.objects.create(
            course_id="CN330",
            course_name="Computer Application Development",
            semester=1,
            academic_year=2020,
            max_seats=3,
            avalibility=True
        )

        # Create students
        Student.objects.create(user=user1)
        Student.objects.create(user=user2)

    def test_admin_page(self):
        # Login admin
        self.client.login(username='admin', password='admin')

        response = self.client.get('/users/')

        # Make sure that admin logged in to admin_index and status code is 200
        self.assertTemplateUsed(response, 'users/admin_index.html')
        self.assertEqual(response.status_code, 200)

        # Make sure there 2 courses are returned
        self.assertEqual(response.context["courses"].count(), 2)

    def test_admin_course_info(self):
        # Login admin
        self.client.login(username='admin', password='admin')

        c1 = Course.objects.get(course_id="CN340")
        s1 = Student.objects.get(pk=1)

        # Enroll student1 to course_id="CN340"
        s1.courses.add(c1)

        response = self.client.get(f'/users/{c1.id}/admin_course')

        # Make sure that status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that these values are returned correctly
        # There only one student who enrolled to this course
        # Therefore, this should returned 1
        self.assertEqual(response.context["students"].count(), 1)
        # There should have 1 out of 2 seats avalible
        self.assertEqual(response.context["avalible_seats"], 1)

    def test_admin_invalid_course_id(self):
        # Login admin
        self.client.login(username='admin', password='admin')

        # Check the response of the course that does not exist
        course_max_id = Course.objects.all().aggregate(Max("id"))["id__max"]
        response = self.client.get(f'/users/{course_max_id + 1}/admin_course')

        # Make sure that status code is 404
        self.assertEqual(response.status_code, 404)