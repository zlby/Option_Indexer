from django.contrib import admin
from client.models import *

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone')
    search_fields = ('user__username',)


@admin.register(OptionCombo)
class OptionComboAdmin(admin.ModelAdmin):
    list_display = ('client',
                    'combo_interval', 'combo_interval')
    search_fields = ('client__user__username', )


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ('time', 'client', 'buy_option_id', 'sell_option_id',
                    'buy_lot', 'sell_lot', 'if_read')
    search_fields = ('client__user__username', )
