# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from option.models import Option

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(to=User)
    email = models.CharField(verbose_name='通知邮箱', max_length=50, null=True)
    phone = models.CharField(verbose_name='通知手机号', max_length=20, null=True)

    def new_combo(self, positive_option_id, negative_option_id):
        if Option.objects.filter(code=positive_option_id).exists() and \
                Option.objects.filter(code=negative_option_id).exists():
            if not OptionCombo.objects.filter(client=self, positive_option_id=positive_option_id,
                                              negative_option_id=negative_option_id).exists():
                OptionCombo.objects.create(client=self, positive_option_id=positive_option_id,
                                           negative_option_id=negative_option_id)
            return True
        else:
            return False

    def delete_combo(self, combo_id):
        try:
            combo = self.optioncombo_set.get(id=combo_id)
        except OptionCombo.DoesNotExist:
            return False
        combo.delete()
        return True

    def get_all_combo(self):
        return list(combo.get_combo_detail()
                    for combo in self.optioncombo_set.all()
                    .select_related('client').select_related('client__user'))

    def get_all_notification(self):
        return list(notice.get_notification_detail() for notice in self.notificationhistory_set.all())


class OptionCombo(models.Model):
    client = models.ForeignKey(to=Client)
    positive_option = models.ForeignKey(to=Option, verbose_name='正向期权', related_name='positive_clients')
    negative_option = models.ForeignKey(to=Option, verbose_name='反向期权', related_name='negative_clients')

    def get_combo_detail(self):
        data = {
            'id': self.id,
            'client': self.client.user.username,
            'positive_option': self.positive_option_id,
            'negative_option': self.negative_option_id,
        }
        return data


class NotificationHistory(models.Model):
    time = models.DateTimeField(verbose_name='提醒发送时间', auto_now_add=True)
    client = models.ForeignKey(to=Client)
    buy_option = models.ForeignKey(to=Option, verbose_name='买入期权', related_name='buy_notification')
    sell_option = models.ForeignKey(to=Option, verbose_name='卖出期权', related_name='sell_notification')
    buy_lot = models.IntegerField(verbose_name='买入手数')
    sell_lot = models.IntegerField(verbose_name='卖出手数')
    if_read = models.BooleanField(verbose_name='是否已读', default=False)

    class Meta:
        ordering = ['-time']

    def get_notification_detail(self):
        data = {
            'id': self.id,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'buy_option': self.buy_option_id,
            'sell_option': self.sell_option_id,
            'buy_lot': self.buy_lot,
            'sell_lot': self.sell_lot,
            'if_read': self.if_read,
        }
        return data
