from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Course, Test, TestData, Comment, Message, Movies

class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "course_name", "get_users","description")
    def get_users(self, obj):
        return "\n".join([user.username for user in obj.users.all()])

class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "test_version", "result", "user", "course")

class TestDataAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "question1", "question2", "question3", "question4", "question5", "question6")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "timestamp", "course")

class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "timestamp", "sender", "read")

class MoviesAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie_id', 'rating')

admin.site.register(Course, CourseAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(TestData, TestDataAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Movies, MoviesAdmin)