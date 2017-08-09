# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as set_session_as_logged, logout as detach_logged_status
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from functools import wraps
from client.models import Client, NotificationHistory


# Create your views here.
def customized_login_required(method):
    """
    自动检测登陆状态并执行错误返回
    :param method:
    :return:
    """
    @wraps(method)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.is_staff:
                # 如果是超级用户就执行登出然后返回未登录状态
                detach_logged_status(request)
                status = {'code': -5, 'message': 'user not logged in'}
                result = {'status': status}
                return JsonResponse(result, status=401)
            else:
                return method(request, *args, **kwargs)
        else:
            # 用户未登陆
            status = {'code': -5, 'message': 'user not logged in'}
            result = {'status': status}
            return JsonResponse(result, status=401)
    return wrapper


def login(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.user.is_authenticated():
        detach_logged_status(request)
    if request.method == 'POST':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        username = request_data.get('username')
        password = request_data.get('password')
        if password and username:
            user = authenticate(username=username, password=password)
            if user:
                set_session_as_logged(request, user)
                status['message'] = 'login success'
                return JsonResponse(result, status=200)
            else:
                status['code'] = -1
                status['message'] = 'username or password is wrong'
                return JsonResponse(result, status=403)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def logout(request):
    detach_logged_status(request)
    status = {'code': 0, 'message': 'logout success'}
    result = {'status': status}
    return JsonResponse(result, status=200)


def new_client(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'POST':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        username = request_data.get('username')
        password = request_data.get('password')
        email = request_data.get('email')
        phone = request_data.get('phone')
        if username and password:
            if User.objects.filter(username=username).exists():
                status['code'] = -3
                status['message'] = 'username has been used'
                return JsonResponse(result, status=409)
            else:
                new_user = User.objects.create_user(username=username, password=password)
                Client.objects.create(user=new_user, email=email, phone=phone)
                set_session_as_logged(request, authenticate(username=username, password=password))
                status['message'] = 'register success'
                return JsonResponse(result, status=200)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def get_client_info(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        user = request.user
        client = user.client
        status['message'] = 'get info success'
        result = {'status': status,
                  'username': user.username,
                  'email': client.email,
                  'phone': client.phone}
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def set_new_password(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'POST':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        old_password = request_data.get('old_password')
        new_password = request_data.get('new_password')
        if old_password and new_password:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                status['message'] = 'change password success'
                return JsonResponse(result, status=200)
            else:
                status['code'] = -4
                status['message'] = 'old password is wrong'
                return JsonResponse(result, status=401)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def set_new_email_phone(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'PUT':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        new_email = request_data.get('email')
        new_phone = request_data.get('phone')
        if new_email or new_phone:
            client = request.user.client
            if new_email:
                client.email = new_email
            if new_phone:
                client.phone = new_phone
            client.save()
            status['message'] = 'set success'
            return JsonResponse(result, status=200)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def new_combo(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'PUT':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        positive_option = request_data.get('positive_option')
        negative_option = request_data.get('negative_option')
        if positive_option and negative_option:
            if request.user.client.new_combo(positive_option, negative_option):
                status['message'] = 'created'
                result['combo_list'] = request.user.client.get_all_combo()
                return JsonResponse(result, status=201)
            else:
                status['code'] = -6
                status['message'] = '期权或期权套利组合不存在'
                return JsonResponse(result, status=404)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def delete_combo(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'PUT':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        combo_id = request_data.get('id')
        if combo_id:
            if request.user.client.delete_combo(combo_id):
                status['message'] = 'combo delete'
                result['combo_list'] = request.user.client.get_all_combo()
                return JsonResponse(result, status=200)
            else:
                status['code'] = -7
                status['message'] = 'combo not found'
                return JsonResponse(result, status=404)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def get_all_combo(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        status['message'] = 'success'
        result['combo_list'] = request.user.client.get_all_combo()
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def get_all_notification(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        status['message'] = 'success'
        result['notification_list'] = request.user.client.get_all_notification()
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


@customized_login_required
def mark_notification_as_read(request, notification_id):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'PUT':
        try:
            notification = request.user.client.notificationhistory_set.get(id=notification_id)
        except NotificationHistory.DoesNotExist:
            status['code'] = 404
            status['message'] = '通知id不存在'
            return JsonResponse(result, status=404)
        notification.if_read = True
        notification.save()
        status['message'] = 'success'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)
