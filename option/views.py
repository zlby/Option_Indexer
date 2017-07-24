from django.http import JsonResponse
import json
from datetime import datetime
from option.models import Future, Option, News, Intervals

# Create your views here.


def get_future_list(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        result['future_list'] = Future.get_future_option_list()
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
        try:
            future = Future.objects.get(code=future_code)
        except Future.DoesNotExist:
            status['code'] = 404
            status['message'] = '期货代码不存在'
            return JsonResponse(result, status=404)
        result['option_list'] = Option.get_option_list(future)
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
        page_number = request.GET.get('page_number', '1')
        if page_number.isdigit():
            page_number = int(page_number)
        else:
            page_number = 1
        result['news'], result['total_page'] = News.get_news(page_number)
        status['message'] = '获取成功'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def get_future_treading_data(request, future_code):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        datetime_format = '%Y-%m-%d %H:%M'
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        if start_time:
            try:
                future = Future.objects.get(code=future_code)
            except Future.DoesNotExist:
                status['code'] = 404
                status['message'] = '期货代码不存在'
                return JsonResponse(result, status=404)
            try:
                start_time = datetime.strptime(start_time, datetime_format)
                if end_time:
                    end_time = datetime.strptime(end_time, datetime_format)
            except ValueError:
                status['code'] = -12
                status['message'] = 'time_format_not_right'
                return JsonResponse(result, status=400)
            status['data'] = future.get_hour_treading_data(start_time=start_time, end_time=end_time)
            status['message'] = '获取成功'
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


def get_option_treading_data(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        datetime_format = '%Y-%m-%d %H:%M'
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        try:
            start_time = datetime.strptime(start_time, datetime_format)
            if end_time:
                end_time = datetime.strptime(end_time, datetime_format)
        except ValueError:
            status['code'] = -12
            status['message'] = 'time_format_not_right'
            return JsonResponse(result, status=400)
        option_list = request.GET.get('option_list')
        try:
            option_list = list(json.loads(option_list))
        except TypeError:
            status['code'] = -12
            status['message'] = 'time_format_not_right'
            return JsonResponse(result, status=400)
        if start_time:
            pass
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
        if start_time:
            pass

    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def get_possible_combo(request, option_code):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        if Option.objects.filter(code=option_code).exists():
            status['message'] = 'success'
            result['possible_combo'] = Intervals.get_possible_combo(option_code)
        else:
            status['code'] = 404
            status['message'] = '期权代码不存在'
            return JsonResponse(result, status=404)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)

