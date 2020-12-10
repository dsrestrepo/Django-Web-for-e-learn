from django.test import TestCase
from .models import Test,Course,User
# Create your tests here.

class FlightTestCase(TestCase):

    def setUp(self):
        # Create users.         
        u1 = User.objects.create(username="test", email="test@test.com", password="test")
        u2 = User.objects.create(username="test2", email="test2@test.com", password="test2")
        
        # Create course.         
        course1 = Course.objects.create(course_name="Statistics")
        course1.users.add(u1)
        
        # Create Test
        test1 = Test.objects.create(user=u1, course=course1, result=8, test_version="starting test")
        test2 = Test.objects.create(user=u2, course=course1, result=8, test_version="starting test")
    
    def test_is_valid_test(self):
        u2 = User.objects.get(username="test2")
        course1 = Course.objects.get(course_name="Statistics")
        t = Test.objects.get(user=u2,course=course1)
        self.assertFalse(t.is_valid_test)
    
    def test_is_valid_test2(self):
        u1 = User.objects.get(username="test")
        course1 = Course.objects.get(course_name="Statistics")
        t = Test.objects.get(user=u1,course=course1)
        self.assertTrue(t.is_valid_test)
    