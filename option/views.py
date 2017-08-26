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
        data_type = request.GET.get('data_type')
        if start_time:
            if data_type in ['day', 'hour', 'minute']:
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
                if data_type == 'minute':
                    status['data'] = future.get_minute_treading_data(start_time=start_time, end_time=end_time)
                elif data_type == 'hour':
                    status['data'] = future.get_hour_treading_data(start_time=start_time, end_time=end_time)
                else:
                    status['data'] = future.get_day_treading_data(start_time=start_time, end_time=end_time)
                status['message'] = '获取成功'
                return JsonResponse(result, status=200)
            else:
                status['code'] = -2
                status['message'] = 'data_type format not right'
                return JsonResponse(result, status=400)
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
        data_type = request.GET.get('data_type')
        option_list = request.GET.get('option_list')
        if start_time and option_list:
            if data_type in ['day', 'hour', 'minute']:
                try:
                    start_time = datetime.strptime(start_time, datetime_format)
                    if end_time:
                        end_time = datetime.strptime(end_time, datetime_format)
                except ValueError:
                    status['code'] = -12
                    status['message'] = 'time_format_not_right'
                    return JsonResponse(result, status=400)
                try:
                    option_list = list(json.loads(option_list))
                except (TypeError, json.JSONDecodeError):
                    status['code'] = -12
                    status['message'] = 'option list format not right'
                    return JsonResponse(result, status=400)
                data = []
                for option_code in option_list:
                    try:
                        option = Option.objects.get(code=option_code)
                    except Option.DoesNotExist:
                        continue
                    if data_type == 'minute':
                        option_data = option.get_minute_treading_data(start_time, end_time)
                    elif data_type == 'hour':
                        option_data = option.get_hour_treading_data(start_time, end_time)
                    else:
                        option_data = option.get_day_treading_data(start_time, end_time)
                    if option_data:
                        data.append(option_data)
                result['data'] = data
                status['message'] = '获取成功'
                return JsonResponse(result, status=200)

            else:
                status['code'] = -2
                status['message'] = 'data_type format not right'
                return JsonResponse(result, status=400)
        else:
            status['code'] = -2
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
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


def get_asset_evaluation(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        datetime_format = '%Y-%m-%d'
        t1 = request.GET.get('t1')
        physicals = request.GET.get('physicals')
        option_list = request.GET.get('option_list')
        future_list = request.GET.get('future_list')
        if t1 and physicals\
                and option_list\
                and future_list:
            try:
                t1 = datetime.strptime(t1, datetime_format)
            except ValueError:
                status['code'] = -12
                status['message'] = 'time_format_not_right'
                return JsonResponse(result, status=400)
            try:
                option_list = list(json.loads(option_list))
            except (TypeError, json.JSONDecodeError):
                status['code'] = -12
                status['message'] = 'option list format not right'
                return JsonResponse(result, status=400)
            try:
                future_list = list(json.loads(future_list))
            except (TypeError, json.JSONDecodeError):
                status['code'] = -12
                status['message'] = 'future list format not right'
                return JsonResponse(result, status=400)
            asset_evaluation_list = []
            result['asset_evaluation_list'] = asset_evaluation_list
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


def get_future_delivery_day_list(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        result['future_list'] = Future.get_future_and_delivery_day_list()
        status['message'] = '获取成功'
        return JsonResponse(result, status=200)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)
