import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Teacher, TeacherBio, EmailMessage
from django.utils import timezone
from django.urls import reverse

# ✅ בדיקות לפונקציות ניהול ביוגרפיה
class TeacherBioViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(username='teacher', password='pass')
        self.teacher = Teacher.objects.create(user=self.teacher_user, expertise='Physics')
        self.bio = TeacherBio.objects.create(user=self.teacher_user, bio='Test bio')

    def test_add_teacher_bio_get(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.get(reverse('add_teacher_bio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/add_bio.html')

    def test_add_teacher_bio_post(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.post(reverse('add_teacher_bio'), {'bio': 'This is my new bio'})
        self.assertRedirects(response, reverse('add_teacher_bio'))
        self.assertTrue(TeacherBio.objects.filter(bio='This is my new bio').exists())

    def test_delete_teacher_bio(self):
        self.client.login(username='teacher', password='pass')
        bio = TeacherBio.objects.create(user=self.teacher_user, bio='To be deleted')
        response = self.client.post(reverse('delete_teacher_bio', args=[bio.id]))
        self.assertRedirects(response, reverse('add_teacher_bio'))
        self.assertFalse(TeacherBio.objects.filter(id=bio.id).exists())


# ✅ בדיקות הודעות מרצה/תלמיד
class MessageViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager = User.objects.create_user(username='admin', password='admin', is_superuser=True)
        self.teacher = User.objects.create_user(username='teacher', password='pass')
        self.student = User.objects.create_user(username='student', password='pass')
        EmailMessage.objects.create(sender=self.manager, receiver=self.student, content='msg1')
        EmailMessage.objects.create(sender=self.manager, receiver=self.teacher, content='msg2')

    def test_student_messages_view(self):
        self.client.login(username='student', password='pass')
        url = reverse('student_messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/student_messages.html')
        self.assertEqual(len(response.context['messages']), 1)

    def test_teacher_messages_view(self):
        self.client.login(username='teacher', password='pass')
        url = reverse('teacher_messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/teacher_messages.html')
        self.assertEqual(len(response.context['messages']), 1)


# ✅ בדיקות עמודים כלליים
class UsersPagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')

   
    def test_contact_users_page(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('contact_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/contact_users.html')
        self.assertIn('users', response.context)
        self.assertFalse(response.context['users'].filter(is_superuser=True).exists())

from users.models import Student, LearningLevel

class EditStudentProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(username='student', password='oldpass', email='old@student.com')
        level = LearningLevel.objects.create(name='Beginner')  # ✅ יצירת רמת לימוד
        self.student = Student.objects.create(user=self.student_user, learning_level=level)  # ✅ שימוש באובייקט

    def test_edit_student_email(self):
        self.client.login(username='student', password='oldpass')
        response = self.client.post(reverse('edit_student_profile'), {
            'current_password': 'oldpass',
            'new_email': 'new@student.com',
        })
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.email, 'new@student.com')
        self.assertRedirects(response, reverse('student_home'))


class EditTeacherProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(username='teacher', password='oldpass', email='old@teacher.com')
        self.teacher = Teacher.objects.create(user=self.teacher_user, expertise='Math')  # הוספה חשובה

    def test_edit_teacher_email(self):
        self.client.login(username='teacher', password='oldpass')
        response = self.client.post(reverse('edit_teacher_profile'), {
            'current_password': 'oldpass',
            'new_email': 'new@teacher.com',
        })
        self.teacher_user.refresh_from_db()
        self.assertEqual(self.teacher_user.email, 'new@teacher.com')
        self.assertRedirects(response, reverse('teacher_home'))

#---------------------------------------------------------------------------

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Student, Teacher, Manager, LearningLevel

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.level = LearningLevel.objects.create(name='Beginner')

    def test_student_signup_page_loads(self):
        response = self.client.get(reverse('student_signup'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_signup_page_loads(self):
        response = self.client.get(reverse('teacher_signup'))
        self.assertEqual(response.status_code, 200)

    def test_manager_signup_page_loads(self):
        response = self.client.get(reverse('manager_signup'))
        self.assertEqual(response.status_code, 200)

    def test_welcome_page_loads(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_after_login_student(self):
        user = User.objects.create_user(username='stu', password='pass')
        Student.objects.create(user=user, learning_level=self.level)
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('student_home'))

    def test_redirect_after_login_teacher(self):
        user = User.objects.create_user(username='teach', password='pass')
        Teacher.objects.create(user=user, expertise='Math')
        self.client.login(username='teach', password='pass')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('teacher_home'))

    def test_redirect_after_login_manager(self):
        user = User.objects.create_user(username='mgr', password='pass')
        Manager.objects.create(user=user)
        self.client.login(username='mgr', password='pass')
        response = self.client.get(reverse('redirect_after_login'))
        self.assertRedirects(response, reverse('manager_home'))

#---------------------------------------------------------------------------19---------

