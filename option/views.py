from django.http import JsonResponse
import json
from option.models import Future, Option, FutureTreadingData, OptionTreadingData, News

# Create your views here.


def get_future_list(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        result['future_list'] = Future.get_future_list()
        status['message'] = '获取成功'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def get_option_list(request, future_code):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        result['option_list'] = Option.get_option_list(future_code)
        status['message'] = '获取成功'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def get_news(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        if not request.body:
            request_data = {}
        else:
            request_data = json.loads(request.body.decode('utf-8'))
        page_number = request_data.get('page_number', 1)
        result['news'] = News.get_news(page_number)
        status['message'] = '获取成功'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)