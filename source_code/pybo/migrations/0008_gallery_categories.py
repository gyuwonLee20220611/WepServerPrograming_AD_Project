from django.db import migrations


GALLERY_CATEGORIES = [
    ('daily', '일상', '친구들과 공유하는 하루 기록'),
    ('food', '맛집', '함께 가고 싶은 음식점과 카페'),
    ('travel', '여행', '여행 사진과 장소 추천'),
    ('hobby', '취미', '취미 활동과 관심사 공유'),
    ('chat', '자유수다', '가볍게 나누는 자유 이야기'),
]


def update_gallery_categories(apps, schema_editor):
    Category = apps.get_model('pybo', 'Category')
    Question = apps.get_model('pybo', 'Question')

    legacy_slugs = ['django', 'python', 'error', 'notice', 'free']
    Category.objects.filter(slug__in=legacy_slugs).delete()

    chat_category = None
    for slug, name, description in GALLERY_CATEGORIES:
        category, _ = Category.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'description': description},
        )
        if slug == 'chat':
            chat_category = category

    if chat_category:
        Question.objects.filter(category__isnull=True).update(category=chat_category)


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0007_auto_20260520_0020'),
    ]

    operations = [
        migrations.RunPython(update_gallery_categories, migrations.RunPython.noop),
    ]
