from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Student, Teacher, Manager, StudentEvent


class UserStoriesTestCase(TestCase):

    def test_signup_student(self):
        response = self.client.post(reverse('student_signup'), {
            'username': 'student1',
            'email': 'student1@example.com',
            'password': 'pass1234',
            'confirm_password': 'pass1234',
            'profile': 'student',
            'bio': 'Loves math'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='student1').exists())
        self.assertTrue(Student.objects.filter(user__username='student1').exists())

    def test_login_student(self):
        user = User.objects.create_user(username='student2', password='pass1234')
        student = Student.objects.create(user=user, bio='Science')
        self.client.force_login(user)

        StudentEvent.objects.create(
            student=student,
            title='Test Event',
            event_type='lesson',
            date=timezone.now().date()
        )

        response = self.client.get(reverse('student_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Click a day to see events')
        self.assertContains(response, 'lesson')

    def test_signup_teacher(self):
        response = self.client.post(reverse('teacher_signup'), {
            'username': 'teacher1',
            'email': 'teacher1@example.com',
            'password': 'pass1234',
            'confirm_password': 'pass1234',
            'profile': 'teacher',
            'expertise': 'Physics'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='teacher1').exists())
        self.assertTrue(Teacher.objects.filter(user__username='teacher1').exists())

    def test_login_teacher(self):
        user = User.objects.create_user(username='teacher2', password='pass1234')
        Teacher.objects.create(user=user, expertise='Biology')
        self.client.force_login(user)
        response = self.client.get(reverse('teacher_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teacher')

    def test_login_admin(self):
        admin_user = User.objects.create_superuser(username='admin1', email='admin@example.com', password='adminpass')
        login_success = self.client.login(username='admin1', password='adminpass')
        self.assertTrue(login_success)

    def test_homepage_student(self):
        user = User.objects.create_user(username='student3', password='pass1234')
        Student.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(reverse('student_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')

    def test_homepage_teacher(self):
        user = User.objects.create_user(username='teacher3', password='pass1234')
        Teacher.objects.create(user=user, expertise='English')
        self.client.force_login(user)
        response = self.client.get(reverse('teacher_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teacher')
