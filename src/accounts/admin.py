from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
	list_display = ('email','date_joined', 'last_login', 'id','is_staff')
	search_fields = ('email',)
	readonly_fields=('date_joined', 'last_login')
	ordering = ('date_joined','email')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)