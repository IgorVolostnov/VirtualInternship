from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fam_user', 'name_user', 'otc_user', 'email_user', 'phone_user', 'last_login_user',
                    'date_joined_user')
    search_fields = ('user__username', 'fam', 'name', 'otc', 'user__email', 'user__last_login',
                     'user__date_joined')
    list_per_page = 20

    @admin.display(description='Фамилия')
    def fam_user(self, obj):
        return obj.fam

    @admin.display(description='Имя')
    def name_user(self, obj):
        return obj.name

    @admin.display(description='Отчество')
    def otc_user(self, obj):
        return obj.otc

    @admin.display(description='Электронная почта')
    def email_user(self, obj):
        return obj.user.email

    email_user.admin_order_field = 'user__email'

    @admin.display(description='Отчество')
    def phone_user(self, obj):
        return obj.phone

    @admin.display(description='Последний визит')
    def last_login_user(self, obj):
        return obj.user.last_login

    last_login_user.admin_order_field = 'user__last_login'

    @admin.display(description='Дата регистрации')
    def date_joined_user(self, obj):
        return obj.user.date_joined

    date_joined_user.admin_order_field = 'user__date_joined'

    def get_ordering(self, request):
        return ('pk',)
