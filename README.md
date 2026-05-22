# Pybo Gallery 실행 안내

이 폴더는 Django 3.0.6 기반 `pybo` 갤러리형 커뮤니티 게시판 소스입니다.

## 권장 실행 환경

- Python 3.8.x
- Django 3.0.6
- SQLite

최신 Python 버전에서는 Django 3.0.6과 호환성 문제가 생길 수 있으므로 Python 3.8.x 환경 사용을 권장합니다.

## 실행 방법

```powershell
cd .\source_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/`로 접속합니다.

## 검증 방법

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

회원가입, 카테고리 초기화, 검색/필터, 북마크 토글에 대한 기본 테스트가 포함되어 있습니다.

## 환경 변수

로컬 실행에서는 별도로 설정할 필요가 없습니다. 필요한 경우 다음 환경 변수로 기본 설정을 덮어쓸 수 있습니다.

- `DJANGO_SECRET_KEY`: Django 비밀 키
- `DJANGO_DEBUG`: `True` 또는 `False`
- `DJANGO_ALLOWED_HOSTS`: 쉼표로 구분한 허용 호스트 목록

운영 환경에 배포할 경우에는 `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`를 환경에 맞게 지정해야 합니다.
