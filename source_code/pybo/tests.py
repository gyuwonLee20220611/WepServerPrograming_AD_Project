from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Category, Question
from .services import BookmarkService, CategoryService, QuestionService


class CategoryServiceTests(TestCase):
    def test_ensure_defaults_creates_gallery_categories(self):
        CategoryService.ensure_defaults()

        self.assertEqual(Category.objects.count(), 5)
        self.assertTrue(Category.objects.filter(slug='chat', name='자유수다').exists())


class QuestionServiceTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='tester', password='password')
        self.category = Category.objects.create(slug='daily', name='일상')
        Question.objects.create(
            author=self.author,
            category=self.category,
            subject='오늘의 기록',
            content='친구들과 산책했습니다.',
            create_date=timezone.now(),
        )

    def test_list_questions_filters_by_category_and_keyword(self):
        questions = QuestionService.list_questions({
            'category': 'daily',
            'kw': '산책',
            'so': 'content',
        })

        self.assertEqual(questions.count(), 1)
        self.assertEqual(questions.first().subject, '오늘의 기록')


class BookmarkServiceTests(TestCase):
    def test_toggle_adds_and_removes_bookmark(self):
        user = User.objects.create_user(username='bookmark_user', password='password')
        author = User.objects.create_user(username='author', password='password')
        question = Question.objects.create(
            author=author,
            subject='북마크 테스트',
            content='내용',
            create_date=timezone.now(),
        )

        self.assertTrue(BookmarkService.toggle(user, question))
        self.assertTrue(question.bookmark_users.filter(pk=user.pk).exists())

        self.assertFalse(BookmarkService.toggle(user, question))
        self.assertFalse(question.bookmark_users.filter(pk=user.pk).exists())
