from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Teacher

class TeacherTest(TestCase):

    def test_teacher_creation(self):
        teacher = Teacher.objects.create(
            name="Rahul",
            subject="Mathematics",
            classes="10",
            location="Medinipur",
            fees=1000,
            phone="1234567890"
        )

        self.assertEqual(teacher.name, "Rahul")