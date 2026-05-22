# Pybo Gallery

점프 투 장고 `pybo` 게시판을 기반으로 확장한 갤러리형 커뮤니티 게시판입니다.

친구들과 일상, 맛집, 여행, 취미 이야기를 카테고리별로 공유하고, 검색/필터, 인기/미답변 질문, 내 활동 대시보드, 좋아하는 게시글 저장 기능을 사용할 수 있습니다.

## 주요 기능

- 갤러리 카테고리 분류
- 검색 및 카테고리 필터
- 내 활동 대시보드
- 인기 질문 / 미답변 질문
- 좋아하는 게시글 북마크
- 마크다운 본문 렌더링
- 답변 등록/수정/추천 후 해당 답변 위치로 이동

## 개발 환경

- Python 3.8.10
- Django 3.0.6
- SQLite
- Windows PowerShell 기준 실행 확인

## 의존성

주요 의존성은 다음과 같습니다.

- `Django==3.0.6`
- `Markdown==3.7`
- `asgiref==3.8.1`
- `pytz==2026.2`
- `sqlparse==0.5.5`

전체 의존성은 `requirements.txt`에 정리했습니다.

## 실행 방법

프로젝트 폴더로 이동합니다.

```powershell
cd "\djangobook-3-12"
```

가상환경을 생성합니다.

```powershell
python -m venv .venv
```

가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

의존성을 설치합니다.

```powershell
pip install -r requirements.txt
```

마이그레이션을 적용합니다.

```powershell
python manage.py migrate
```

개발 서버를 실행합니다.

```powershell
python manage.py runserver
```

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:8000/
```

## 검증 방법

Django 설정과 앱 구성을 점검합니다.

```powershell
python manage.py check
```

마이그레이션 누락 여부를 확인합니다.

```powershell
python manage.py makemigrations --check --dry-run
```

테스트 명령을 실행합니다.

```powershell
python manage.py test
```

현재 프로젝트에는 별도 자동 테스트 케이스가 없어 `Ran 0 tests`로 표시될 수 있습니다. 기능 검증은 시연 영상에서 주요 기능 흐름을 직접 확인하도록 구성했습니다.

## 환경 변수

별도로 설정해야 하는 환경 변수는 없습니다.

현재 개발용 설정은 `config/settings.py`에 포함되어 있습니다.

- `DEBUG = True`
- `DATABASES`: SQLite 사용
- `LANGUAGE_CODE = 'ko-kr'`
- `TIME_ZONE = 'Asia/Seoul'`
- `LOGIN_REDIRECT_URL = '/'`
- `LOGOUT_REDIRECT_URL = '/'`

운영 환경에 배포할 경우에는 `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, 데이터베이스 설정을 환경 변수 기반으로 분리하는 것이 좋습니다.

## 주요 URL

- `/` 또는 `/pybo/`: 게시글 목록, 검색, 카테고리 필터
- `/pybo/question/create/`: 질문 작성
- `/pybo/<question_id>/`: 질문 상세
- `/pybo/discover/`: 인기 질문 / 미답변 질문
- `/pybo/dashboard/`: 내 활동 대시보드
- `/common/login/`: 로그인
- `/common/signup/`: 회원가입

## 제출 관련 문서

- `A안_신규서비스_구현정리.md`: A안 신규 서비스 및 교과서 기능 구현 정리
- `시연영상_순서.md`: 시연 영상 촬영 순서
- `시연영상_대본.md`: 시연 영상 설명 대본
- `웹서버_프레임워크_비교_리포트.md`: 웹서버 프레임워크 비교 리포트 초안
