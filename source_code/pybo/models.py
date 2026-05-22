from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.CharField(max_length=120, blank=True)

    @classmethod
    def default_names(cls) -> list:
        # 갤러리 게시판에서 기본으로 제공하는 카테고리 이름이다.
        return ['일상', '맛집', '여행', '취미', '자유수다']

    @classmethod
    def default_slug(cls) -> str:
        # 기존 글이나 카테고리가 없는 글은 자유수다로 묶는다.
        return 'chat'

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    # 사용자가 다시 보고 싶은 게시글을 개인 북마크로 저장하기 위한 필드이다.
    bookmark_users = models.ManyToManyField(User, related_name='bookmark_question', blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
