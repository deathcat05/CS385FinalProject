
def create_user(username, password='cs385password', is_root=False):
    from django.contrib.auth.models import User
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, password=password)

        if is_root:
            user.is_superuser=True
            user.is_staff=True
        user.save()


create_user('root', is_root=True)

for i in range(1, 10 + 1):
    username = 'test_user_' + str(i)
    create_user(username)

