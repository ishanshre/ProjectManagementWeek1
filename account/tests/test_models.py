from django.contrib.auth import get_user_model
from django.test import TestCase

from account.models import Department, Profile

User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        self.user_cred = {
            "username": "test",
            "password": "test",
            "email": "test@gmail.com",
        }

    def test_create_normal_user_success(self):
        user = User.objects.create_user(**self.user_cred)
        self.assertEqual(user.username, self.user_cred["username"])
        self.assertEqual(user.email, self.user_cred["email"])
        self.assertTrue(user.check_password(self.user_cred["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_profile_create_success_when_user_create_success(self):
        user = User.objects.create_user(**self.user_cred)
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, self.user_cred["username"])
        self.assertEqual(profile.id, user.profile.id)

    def test_create_superuser_success(self):
        superuser = User.objects.create_superuser(**self.user_cred)
        self.assertEqual(superuser.username, self.user_cred["username"])
        self.assertEqual(superuser.email, self.user_cred["email"])
        self.assertTrue(superuser.check_password(self.user_cred["password"]))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_profile_create_sucess_on_superuser_create(self):
        superuser = User.objects.create_superuser(**self.user_cred)
        profile = Profile.objects.get(user=superuser)
        self.assertEqual(profile.user.username, superuser.username)
        self.assertEqual(profile.user.email, superuser.email)

    def test_department_create_success(self):
        name = "Backend"
        department = Department.objects.create(name=name)
        self.assertEqual(department.name, name)
