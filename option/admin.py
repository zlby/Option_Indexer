from django.contrib import admin
from option.models import  *

# Register your models here.


@admin.register(Future)
class FutureAdmin(admin.ModelAdmin):
    list_display = ('code', 'delivery_day',)
    search_fields = ('code',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('code', 'asset_id',)
    search_fields = ('code', )


class TreadingDataBaseAdmin(admin.ModelAdmin):
    list_display = ('time', 'open_price', 'max_price', 'min_price', 'close_price')


class FutureTreadingDataBaseAdmin(TreadingDataBaseAdmin):
    list_display = TreadingDataBaseAdmin.list_display + ('future_id', )


@admin.register(FutureTreadingData)
class FutureTreadingDataAdmin(FutureTreadingDataBaseAdmin):
    pass


@admin.register(HourFutureTreadingData)
class HourFutureTreadingDataAdmin(FutureTreadingDataBaseAdmin):
    pass


@admin.register(DayFutureTreadingData)
class DayFutureTreadingDataAdmin(FutureTreadingDataBaseAdmin):
    pass


class OptionTreadingDataBaseAdmin(TreadingDataBaseAdmin):
    list_display = TreadingDataBaseAdmin.list_display + ('option_id', 'volatility', 'volume')


@admin.register(OptionTreadingData)
class OptionTreadingDataAdmin(OptionTreadingDataBaseAdmin):
    pass


@admin.register(HourOptionTreadingData)
class HourOptionTreadingDataAdmin(OptionTreadingDataBaseAdmin):
    pass


@admin.register(DayOptionTreadingData)
class DayOptionTreadingDataAdmin(OptionTreadingDataBaseAdmin):
    pass


@admin.register(Intervals)
class IntervalsAdmin(admin.ModelAdmin):
    list_display = ('positive_option', 'negative_option', 'lower_bound_a', 'upper_bound_a',
                    'lower_bound_b', 'upper_bound_b', 'lower_bound_c', 'upper_bound_c', 'rate')
    search_fields = ('positive_option', 'negative_option',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'time',)
