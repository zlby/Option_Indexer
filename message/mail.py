import time
import hmac
import base64
import hashlib
from urllib.parse import quote
import requests
import uuid


class MailSender(object):
    url = 'https://dm.aliyuncs.com'
    ACCESS_KEY_ID = 'LTAIYr8Zt9oFLFID'
    ACCESS_KRY_SECRET = 'ouOJVJH6wiKeyIvsCZjjlaPLLFV92A'
    Action = 'SingleSendMail'
    AccountName = 'service@optionindexer.com'
    ReplyToAddress = False
    AddressType = 1
    FromAlias = 'INDEXER智能⾦金融咨询公司'
    Version = '2015-11-23'
    text_message_base = '尊敬的客户%s您好！\n' \
                '基于您的选择和市场行情的变动，给您建议如下：\n' \
                '\t买入期权代码：%s \n' \
                '\t卖出期权代码：%s \n' \
                '\t买入\卖出手数比：%s \n' \
                '\t套利区间：%s \n' \
                '希望我们的建议为您带来收益。INDEXER智能⾦金融咨询公司竭诚为您服务。 \n'
    text_hedging_base = '尊敬的客户%s您好！\n' \
                '基于您的选择和市场行情的变动，给您建议如下：\n' \
                '\t买入期权代码：%s \n' \
                '\t买入手数：%s \n'  \
                '\t卖出期权代码：%s \n' \
                '\t买入\卖出手数比：%s \n' \
                '希望我们的建议为您带来收益。INDEXER智能⾦金融咨询公司竭诚为您服务。 \n'

    @staticmethod
    def send_message(email, name, buy_option, sell_option, rate, interval):
        text = MailSender.text_message_base % (name, buy_option, sell_option, rate, interval)
        params = {
            'Action': MailSender.Action,
            'AccountName': MailSender.AccountName,
            'ReplyToAddress': MailSender.ReplyToAddress,
            'AddressType': MailSender.AddressType,
            'ToAddress': email,
            'FromAlias': MailSender.FromAlias,
            'Subject': '期权套利提醒',
            'Version': MailSender.Version,
            'TextBody': text,
            'AccessKeyId': MailSender.ACCESS_KEY_ID,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
        }
        params['Signature'] = MailSender.get_signature(params)
        print(params)
        response = requests.get(MailSender.url, params)
        print(response.status_code)
        print(response.text)

    @staticmethod
    def send_hedging_result(email, name, buy_option, sell_option, rate, interval):
        text = MailSender.text_hedging_base % (name, buy_option, sell_option, rate, interval)
        params = {
            'Action': MailSender.Action,
            'AccountName': MailSender.AccountName,
            'ReplyToAddress': MailSender.ReplyToAddress,
            'AddressType': MailSender.AddressType,
            'ToAddress': email,
            'FromAlias': MailSender.FromAlias,
            'Subject': '期权套利提醒',
            'Version': MailSender.Version,
            'TextBody': text,
            'AccessKeyId': MailSender.ACCESS_KEY_ID,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
        }
        params['Signature'] = MailSender.get_signature(params)
        print(params)
        response = requests.get(MailSender.url, params)
        print(response.status_code)
        print(response.text)

    @staticmethod
    def percent_encode(target_str):
        target_str = str(target_str)
        res = quote(target_str, '') \
            .replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
        return res

    @staticmethod
    def get_signature(params):
        sorted_params = sorted(params.items(), key=lambda parameters: parameters[0])
        formed_query_string = ''
        for param in sorted_params:
            formed_query_string += '&' + MailSender.percent_encode(param[0]) + '=' + MailSender.percent_encode(param[1])
        string_to_sign = 'GET&%2F&' + MailSender.percent_encode(formed_query_string[1:])
        h = hmac.new((MailSender.ACCESS_KRY_SECRET + '&').encode(), string_to_sign.encode(), hashlib.sha1)
        signature = base64.encodebytes(h.digest()).strip()
        return signature




