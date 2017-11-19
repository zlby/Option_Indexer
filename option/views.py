from django.http import JsonResponse
import json
from datetime import datetime
from option.models import Future, Option, News, Intervals
from client.models import Client
from message.mail import MailSender
from gain_loss import asset_portfolio
from hedging import monte_carlo_stimulation, spot_price_distribution
from cross_breed_hedge import cross_breed


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
        if t1 and physicals \
                and option_list \
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
            asset_evaluation_list = asset_portfolio.get_ass(t1, physicals, future_list, option_list)
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


def get_distribution(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        dis_type = request.GET.get('type')
        datetime_format = '%Y-%m-%d'
        time_future = request.GET.get('time_future')
        argv = request.GET.get('argv')
        argv = list(json.loads(argv))
        if dis_type and argv:
            if dis_type == "normal":
                result['distribution'] = spot_price_distribution.show_normal_distribution(argv[0], argv[1])
            elif dis_type == "triangle":
                result['distribution'] = spot_price_distribution.show_triangle_distribution(argv[0], argv[1], argv[2])
            elif dis_type == "uniform":
                result['distribution'] = spot_price_distribution.show_uniform_distribution(argv[0], argv[1])
            elif dis_type == "predict":
                if time_future:
                    try:
                        time_future = datetime.strptime(time_future, datetime_format)
                    except ValueError:
                        status['code'] = -12
                        status['message'] = 'time format not right'
                        return JsonResponse(result, status=400)
                    result['distribution'] = spot_price_distribution.show_predict(time_future)
                else:
                    status['code'] = -12
                    status['message'] = 'no time provided'
                    return JsonResponse(result, status=400)
            status['message'] = '获取成功'
            return JsonResponse(result, status=200)
        else:
            status['code'] = -24
            status['message'] = 'need more argument'
            return JsonResponse(result, status=400)
    else:
        # http方法不支持
        status['code'] = 405
        status['message'] = 'http method not supported'
        return JsonResponse(result, status=405)


def get_hedging(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        datetime_format = '%Y-%m-%d'
        future_list = request.GET.get('future_list')
        option_list = request.GET.get('option_list')
        physicals = request.GET.get('physicals')
        w1 = request.GET.get('w1')
        w2 = request.GET.get('w2')
        time_future = request.GET.get('time_future')
        dist = request.GET.get('dist')
        max_cost = request.GET.get('max_cost')
        fmax = request.GET.get('fmax')
        omax = request.GET.get('omax')

        if future_list and option_list \
                and physicals \
                and w1 and w2 \
                and time_future \
                and dist:
            try:
                time_future = datetime.strptime(time_future, datetime_format)
            except ValueError:
                status['code'] = -12
                status['message'] = 'time format not right'
                return JsonResponse(result, status=400)
            try:
                future_list = list(json.loads(future_list))
            except (TypeError, json.JSONDecodeError):
                status['code'] = -12
                status['message'] = 'future list format not right'
                return JsonResponse(result, status=400)
            try:
                option_list = list(json.loads(option_list))
            except (TypeError, json.JSONDecodeError):
                status['code'] = -12
                status['message'] = 'option list format not right'
                return JsonResponse(result, status=400)

            try:
                dist = dict(json.loads(dist))
                dist['argv'] = list(dist['argv'])
            except (TypeError, json.JSONDecodeError):
                status['code'] = -12
                status['message'] = 'dist format not right'
                return JsonResponse(result, status=400)

            if not isinstance(max_cost, float):
                max_cost = 50000
            if not isinstance(fmax, int):
                fmax = 50
            if not isinstance(omax, int):
                omax = 50

            future_r, option_r = \
                monte_carlo_stimulation.monte_carlo(future_list, option_list, physicals,
                                                    w1, w2, time_future, dist, max_cost, fmax, omax)
            result['future_list'] = future_r
            result['option_list'] = option_r
            status['message'] = 'Success'

            user = request.user
            if user.is_authenticated:
                client = Client.objects.get(user=user)
                MailSender.send_hedging_result(client.email, client.user.username, future_r, option_r)

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


def choose_future(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        datetime_format = '%Y-%m-%d'
        agri_type = request.GET.get('agri_type')
        time_future = request.GET.get('time_future')

        if agri_type and time_future:
            try:
                time_future = datetime.strptime(time_future, datetime_format)
            except ValueError:
                status['code'] = -12
                status['message'] = 'time_format_not_right'
                return JsonResponse(result, status=400)
            result['future_return'] = cross_breed.choose_futures(agri_type, time_future)
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


def get_cross_breed_hedge(request):
    status = {'code': 0, 'message': 'unknown'}
    result = {'status': status}
    if request.method == 'GET':
        agri_type = request.GET.get('agri_type')
        code = request.GET.get('code')

        if agri_type and code:
            crop_r = cross_breed.show_crop_diagram(agri_type)
            future_r = cross_breed.show_future_diagram(code)
            error_r = cross_breed.show_error_diagram(agri_type, code)
            result['future_list'] = future_r
            result['crop_list'] = crop_r
            result['error_list'] = error_r
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
