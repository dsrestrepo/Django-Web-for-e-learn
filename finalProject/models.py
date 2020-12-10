from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthdate = models.DateField(auto_now=False, blank=True, null=True)
    career = models.CharField(blank=True, max_length=30)
    country = models.CharField(blank=True, max_length=30)
    profession = models.CharField(blank=True, max_length=30)
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    pass

class Course(models.Model):
    couses_names = [
        ('Statistics', 'Statistics'),
        ('Computer Science', 'Computer Science'),
        ('Data Science', 'Data Science'),
        ('Communications', 'Communications'),
        ('Social', 'Social'),
        ('other', 'other')
    ]
    course_name = models.CharField(max_length=16, choices=couses_names, default="other",unique=True)
    description = models.TextField(default=f"We hope you'll enjoy and learn in this course")
    users = models.ManyToManyField(User, blank=True, related_name="course")
    def __str__(self):
        return f"{self.course_name}"
    def serialize(self):
        return {
            "id": self.id,
            "course_name": self.course_name,
            "description": self.description
        }

class Test(models.Model):
    tests = [
        ('1', 'Starting test'),
        ('2', 'second test'),
        ('3', 'final test')
    ]
    test_version = models.CharField(max_length=8, choices=tests, default='1')
    result = models.IntegerField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="course_results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="course_results")
    def __str__ (self):
        return f"the student {self.user} has a {self.result} in the {self.test_version} of the {self.course} course"
    def is_valid_test(self):    
        try:
            user=self.course.objects.get(users=self.user)
        except self.course.DoesNotExist:
            user=False        
        if user:
            user=True
        return user
    def serialize(self):
        return {
            "id": self.id,
            "test_version": self.test_version,
            "result": self.result,
            "user":self.user
        }

class TestData(models.Model):
    answer = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('NA','NA')
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test_data")
    question1 = models.CharField(max_length=2, choices=answer, default='NA')
    question2 = models.CharField(max_length=2, choices=answer, default='NA')
    question3 = models.CharField(max_length=2, choices=answer, default='NA')
    question4 = models.CharField(max_length=2, choices=answer, default='NA')
    question5 = models.CharField(max_length=2, choices=answer, default='NA')
    question6 = models.CharField(max_length=2, choices=answer, default='NA')
    def __str__(self):
        return f"the student {self.test.user} has response the examen {self.test.test_version} for {self.test.course}"
    def serialize(self):
        return {
            "id": self.id,
            "test": self.test,
            "question1": self.question1,
            "question2": self.question2,
            "question3": self.question3,
            "question4": self.question4,
            "question5": self.question5,
            "question6": self.question6,
        }

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
    def __str__(self):
        return f"post {self.id} by user: {self.user} at: {self.timestamp}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")

    read = models.BooleanField(default=False)
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "sender": self.sender,
            "read":self.read
        }
    def __str__(self):
        return f"post {self.id} by user: {self.user} at: {self.timestamp}"


class Movies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    movie_id = models.IntegerField(primary_key=True)
    rating = models.IntegerField(blank=False)

    def serialize(self):
        return {
            "id": self.movie_id,
            "rating": self.rating,
            "user": self.user
        }
    def __str__(self):
        return f"movie {self.movie_id} rated with: {self.rating} by: {self.user}"
