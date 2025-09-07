from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Habit

User = get_user_model()

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Выпить стакан воды",
            execution_time=60,
            periodicity=1
        )
        self.assertEqual(habit.action, "Выпить стакан воды")

    def test_habit_str(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Выпить стакан воды",
            execution_time=60,
            periodicity=1
        )
        expected_str = f"{self.user} - Выпить стакан воды"
        self.assertEqual(str(habit), expected_str)

# tests/test_api.py
class HabitAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_habit(self):
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "execution_time": 60,
            "periodicity": 1
        }
        response = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)

    # Добавьте больше тестов...
