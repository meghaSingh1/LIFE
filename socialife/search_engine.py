from .models import MyUser

class Search:
    def __init__(self):
        self.result = None

    def search_by_profile_name(self, profile_name, auto_completion=False):
        if not auto_completion:
            user = MyUser.objects.filter(profile_name=profile_name)
        else:
            user = MyUser.objects.filter(profile_name__icontains=profile_name)
        if len(user) > 0:
            self.result = user
        return self

    def search_by_name(self, name):
        users = MyUser.objects.objects.all()
        name_array = name.split()
        for user in users:
            relative = 0
            full_name = user.first_name + ' ' + user.last_name
            for word in name_array:
                if word in full_name:
                    relative = relative + 1
            user.relative = relative
        if len(users) > 0:
            self.result = users
        return self
