from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q

from .models import Answer, Category, Comment, Question


DEFAULT_CATEGORIES = [
    ('daily', '일상', '친구들과 공유하는 하루 기록'),
    ('food', '맛집', '함께 가고 싶은 음식점과 카페'),
    ('travel', '여행', '여행 사진과 장소 추천'),
    ('hobby', '취미', '취미 활동과 관심사 공유'),
    ('chat', '자유수다', '가볍게 나누는 자유 이야기'),
]


class CategoryService:
    @classmethod
    def ensure_defaults(cls) -> None:
        # 기본 카테고리가 없을 때 자동으로 생성해 초기 실행을 쉽게 한다.
        for slug, name, description in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': description},
            )

    @classmethod
    def list_categories(cls):
        cls.ensure_defaults()
        return Category.objects.order_by('name')


class QuestionService:
    @classmethod
    def list_questions(cls, params):
        # request.GET으로 받은 검색 조건을 서비스 계층에서 해석한다.
        CategoryService.ensure_defaults()
        question_list = (
            Question.objects.select_related('author', 'category')
            .annotate(answer_count=Count('answer', distinct=True), vote_count=Count('voter', distinct=True))
            .order_by('-create_date')
        )

        category = params.get('category', '')
        keyword = params.get('kw', '').strip()
        search_type = params.get('so', 'all')

        if category:
            question_list = question_list.filter(category__slug=category)

        if keyword:
            if search_type == 'subject':
                query = Q(subject__icontains=keyword)
            elif search_type == 'content':
                query = Q(content__icontains=keyword)
            elif search_type == 'author':
                query = Q(author__username__icontains=keyword)
            else:
                query = (
                    Q(subject__icontains=keyword)
                    | Q(content__icontains=keyword)
                    | Q(author__username__icontains=keyword)
                    | Q(answer__content__icontains=keyword)
                )
            question_list = question_list.filter(query).distinct()

        return question_list

    @classmethod
    def popular_questions(cls):
        # 추천 수와 답변 수를 기준으로 친구들이 많이 반응한 글을 보여준다.
        return (
            Question.objects.select_related('author', 'category')
            .annotate(vote_count=Count('voter', distinct=True), answer_count=Count('answer', distinct=True))
            .order_by('-vote_count', '-answer_count', '-create_date')[:10]
        )

    @classmethod
    def unanswered_questions(cls):
        # 아직 대화가 시작되지 않은 글을 모아 참여를 유도한다.
        return (
            Question.objects.select_related('author', 'category')
            .annotate(answer_count=Count('answer', distinct=True))
            .filter(answer_count=0)
            .order_by('-create_date')[:20]
        )


class BookmarkService:
    @classmethod
    def toggle(cls, user: User, question: Question) -> bool:
        # 이미 저장한 글이면 해제하고, 저장하지 않은 글이면 북마크에 추가한다.
        if not user.is_authenticated:
            raise PermissionDenied('Login is required.')

        if question.bookmark_users.filter(pk=user.pk).exists():
            question.bookmark_users.remove(user)
            return False

        question.bookmark_users.add(user)
        return True


class DashboardService:
    @classmethod
    def user_summary(cls, user: User) -> dict:
        # auth의 request.user를 기준으로 개인 활동 데이터를 집계한다.
        if not user.is_authenticated:
            raise PermissionDenied('Login is required.')

        questions = Question.objects.filter(author=user)
        answers = Answer.objects.filter(author=user)
        comments = Comment.objects.filter(author=user)
        bookmarked_questions = Question.objects.filter(bookmark_users=user).select_related('author', 'category')

        return {
            'question_count': questions.count(),
            'answer_count': answers.count(),
            'comment_count': comments.count(),
            'bookmark_count': bookmarked_questions.count(),
            'received_votes': sum(question.voter.count() for question in questions),
            'recent_questions': questions.order_by('-create_date')[:5],
            'recent_answers': answers.select_related('question').order_by('-create_date')[:5],
            'recent_comments': comments.order_by('-create_date')[:5],
            'bookmarked_questions': bookmarked_questions.order_by('-create_date')[:10],
        }
