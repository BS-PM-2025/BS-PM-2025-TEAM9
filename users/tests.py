from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Teacher, TeacherBio, EmailMessage, Student, LearningLevel, Manager

# -----------------------------
# Login / Logout Tests
# -----------------------------

class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # should redirect after login

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password', status_code=200)

    def test_logout_redirects(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('welcome'))

# -----------------------------
# Welcome Page Tests
# -----------------------------

class WelcomePageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_welcome_page_anonymous(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/welcome.html')

# -----------------------------
# Signup Tests
# -----------------------------

class SignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.level = LearningLevel.objects.create(name='Beginner')

    def test_student_signup_page_loads(self):
        response = self.client.get(reverse('student_signup'))
        self.assertEqual(response.status_code, 200)

    def test_student_signup_post(self):
        response = self.client.post(reverse('student_signup'), {
            'username': 'newstudent',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'learning_level': self.level.id,
        })
        self.assertEqual(User.objects.filter(username='newstudent').count(), 1)

    def test_teacher_signup_page_loads(self):
        response = self.client.get(reverse('teacher_signup'))
        self.assertEqual(response.status_code, 200)

    def test_manager_signup_page_loads(self):
        response = self.client.get(reverse('manager_signup'))
        self.assertEqual(response.status_code, 200)

# -----------------------------
# Home Pages Tests
# -----------------------------

class HomePagesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.level = LearningLevel.objects.create(name='Beginner')

        self.manager = User.objects.create_user(username='manager', password='testpass', is_superuser=True)

        self.teacher_user = User.objects.create_user(username='teacher_home', password='pass')
        Teacher.objects.create(user=self.teacher_user, expertise='Biology')

        self.student_user = User.objects.create_user(username='student_home', password='pass')
        Student.objects.create(user=self.student_user, learning_level=self.level)

    def test_manager_home_page_loads(self):
        self.client.login(username='manager', password='testpass')
        response = self.client.get(reverse('manager_home'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_home_page_loads(self):
        self.client.login(username='teacher_home', password='pass')
        response = self.client.get(reverse('teacher_home'))
        self.assertEqual(response.status_code, 200)

    def test_student_home_page_loads(self):
        self.client.login(username='student_home', password='pass')
        response = self.client.get(reverse('student_home'))
        self.assertEqual(response.status_code, 200)

# -----------------------------
# Profile Edit Tests
# -----------------------------

class ProfileEditTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(username='teacher_edit', password='pass', email='old@teacher.com')
        self.teacher = Teacher.objects.create(user=self.teacher_user, expertise='Math')

        self.level = LearningLevel.objects.create(name='Beginner')
        self.student_user = User.objects.create_user(username='student_edit', password='pass', email='old@student.com')
        self.student = Student.objects.create(user=self.student_user, learning_level=self.level)

    def test_edit_teacher_email(self):
        self.client.login(username='teacher_edit', password='pass')
        response = self.client.post(reverse('edit_teacher_profile'), {
            'current_password': 'pass',
            'new_email': 'new@teacher.com',
        })
        self.teacher_user.refresh_from_db()
        self.assertEqual(self.teacher_user.email, 'new@teacher.com')
        self.assertRedirects(response, reverse('teacher_home'))

    def test_edit_student_email(self):
        self.client.login(username='student_edit', password='pass')
        response = self.client.post(reverse('edit_student_profile'), {
            'current_password': 'pass',
            'new_email': 'new@student.com',
        })
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.email, 'new@student.com')
        self.assertRedirects(response, reverse('student_home'))

# -----------------------------
# Contact Users Page Tests
# -----------------------------

class ContactUsersViewTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', password='testpass', is_superuser=True)

        teacher_user1 = User.objects.create_user(username='teacher1', email='teacher1@example.com', password='testpass')
        Teacher.objects.create(user=teacher_user1, expertise='Math')

        level = LearningLevel.objects.create(name='Beginner')

        student_user1 = User.objects.create_user(username='student1', email='student1@example.com', password='testpass')
        Student.objects.create(user=student_user1, learning_level=level)

        self.client = Client()
        self.client.login(username='manager', password='testpass')

    def test_contact_users_view_status_code(self):
        response = self.client.get(reverse('contact_users'))
        self.assertEqual(response.status_code, 200)

# -----------------------------
# Student Messages Tests
# -----------------------------

class StudentMessagesViewTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username='manager', password='testpass', is_superuser=True)

        teacher_user = User.objects.create_user(username='teacher1', email='teacher1@example.com', password='testpass')
        Teacher.objects.create(user=teacher_user, expertise='Math')

        level = LearningLevel.objects.create(name='Beginner')

        student_user = User.objects.create_user(username='student1', email='student1@example.com', password='testpass')
        Student.objects.create(user=student_user, learning_level=level)

        self.client = Client()
        self.client.login(username='student1', password='testpass')

    def test_student_messages_view_status_code(self):
        response = self.client.get(reverse('student_messages'))
        self.assertEqual(response.status_code, 200)

# -----------------------------
# Static Pages Tests
# -----------------------------

class StaticPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

# Add tests for terms/privacy if needed

# -----------------------------
# Unauthorized Access Tests
# -----------------------------

class UnauthorizedAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.level = LearningLevel.objects.create(name='Beginner')
        self.teacher_user = User.objects.create_user(username='teacher_noauth', password='pass')
        Teacher.objects.create(user=self.teacher_user, expertise='Chemistry')
        self.student_user = User.objects.create_user(username='student_noauth', password='pass')
        Student.objects.create(user=self.student_user, learning_level=self.level)

    def test_add_teacher_bio_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_teacher_bio'))
        self.assertRedirects(response, f"/login/?next={reverse('add_teacher_bio')}")

    def test_student_messages_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('student_messages'))
        self.assertRedirects(response, f"/login/?next={reverse('student_messages')}")

    def test_contact_users_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('contact_users'))
        self.assertRedirects(response, f"/login/?next={reverse('contact_users')}")
