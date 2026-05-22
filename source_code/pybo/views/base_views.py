from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Question
from ..services import BookmarkService, CategoryService, DashboardService, QuestionService


def index(request):
    page = request.GET.get('page', '1')
    # 검색어, 검색 대상, 카테고리 값은 request.GET으로 전달받는다.
    question_list = QuestionService.list_questions(request.GET)
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'category_list': CategoryService.list_categories(),
        'selected_category': request.GET.get('category', ''),
        'kw': request.GET.get('kw', ''),
        'so': request.GET.get('so', 'all'),
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def dashboard(request):
    # 로그인한 사용자 기준으로 개인 활동과 북마크 목록을 보여준다.
    context = DashboardService.user_summary(request.user)
    return render(request, 'pybo/dashboard.html', context)


def discover(request):
    # 갤러리 게시판에서 반응이 많은 글과 아직 답변이 없는 글을 분리해 보여준다.
    context = {
        'popular_questions': QuestionService.popular_questions(),
        'unanswered_questions': QuestionService.unanswered_questions(),
    }
    return render(request, 'pybo/discover.html', context)


@login_required(login_url='common:login')
def bookmark(request, question_id):
    # 상세 화면의 저장 버튼을 누르면 북마크 추가/해제를 토글한다.
    question = get_object_or_404(Question, pk=question_id)
    is_bookmarked = BookmarkService.toggle(request.user, question)
    if is_bookmarked:
        messages.success(request, '좋아하는 게시글에 저장했습니다.')
    else:
        messages.success(request, '좋아하는 게시글에서 해제했습니다.')
    return redirect('pybo:detail', question_id=question.id)
