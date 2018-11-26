from django.contrib.auth.models import User

if not User.objects.filter(username='root').exists():
    user = User.objects.create_user('root', password='cs385root')
    user.is_superuser=True
    user.is_staff=True
    user.save()
