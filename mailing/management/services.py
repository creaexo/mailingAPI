
import time
from datetime import timedelta, datetime
import requests, json
from django.utils import timezone

from celery_app import app
from management.models import Client, Message, Mailing


# from .models import *

def w(dt_start, dt_end):
    pass

@app.task()
def send_message(id_message: int, phone: int, text: str, url: str = 'https://probe.fbrq.cloud/v1/send/',
                 token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAzMDAwNjIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9zMTFnbnVtIn0.y6PCjdipXQZ9q21odrXvjlJmiD6KSgqunUAPcpqSZ-c'):
    """
        A function that sends messages to an external server via API. Executed in the background due to app celery

        id_message - id of new message
        phone - client phone number
        text - message text
        url - url address to send the request. If you don't use the default value, don't forget to specify "/" at the end
        token - unique token for sending messages to external api

    """
    url = url + str(id_message)
    headers = {
        'accept': 'application/json',
        'Authorization': f'{token}',
        'Content-Type': 'application/json',
    }
    data = {
        "id": id_message,
        "phone": phone,
        "text": f"{text}"
    }
    json_data = json.dumps(data)
    try:
        response = requests.post(url, data=json_data, headers=headers).json()
        return response['message']
    except requests.exceptions.ConnectionError as e:
        return e


@app.task(bind=True)
def test_task(self):
    pass

@app.task()
def start_mailing1(mailing_id: int, mailing_user: int, dt_start: str, dt_end: str, text: str, tag_filter: str,
                   operator_code_filter: str, stopped: bool):
    """
        Mailing start function. Executed in the background due to app celery

        mailing_id - id of new mailing
        mailing_user - service user who created the mailing
        dt_start - the date and time of the mailing start. The value takes into account the local client time
        dt_end - the date and time when the mailing ends. The value takes into account the local client time
        text - text of mailing
        tag_filter - tags of users to whom messages will be sent. Specify in the format "900;901;902...".
        If not specified, users with and without all tags will
        be selected
        operator_code_filter - operator codes of users to whom messages will be sent. Specify in the format
        "900;901;902...". If not specified, users with all codes will be selected
        stopped - A mark indicating whether the mailing has been stopped
    """
    # Filter separation
    tag_filter = tag_filter.split(';')
    operator_code_filter = operator_code_filter.split(';')
    # End of mailing for users with the last time zone
    end = dt_end + timedelta(hours=23)
    # Filter for suitable time zones
    time_zone_filter = []
    excluded_users_id = []
    if stopped:
        excluded_users_list = list(Message.objects.filter(mailing_id=mailing_id).values())
        for i in excluded_users_list:
            excluded_users_id.append(i['client_id'])
    for i in range(24):
        if dt_end > (timezone.now()+timedelta(hours=i)):
            time_zone_filter.append(i)
    # Creating a list by filters
    if tag_filter != [''] and operator_code_filter != ['']:
        model = Client.objects.filter(
            user=mailing_user, tag__in=tag_filter, operator_code__in=operator_code_filter,
            time_zone__in=time_zone_filter).values().exclude(id__in=excluded_users_id).order_by('time_zone')
    elif tag_filter != [''] and operator_code_filter == ['']:
        model = Client.objects.filter(
            user=mailing_user, tag__in=tag_filter,
            time_zone__in=time_zone_filter).values().exclude(id__in=excluded_users_id).order_by('time_zone')
    elif operator_code_filter != [''] and tag_filter == ['']:
        model = Client.objects.filter(
            user=mailing_user, operator_code__in=operator_code_filter,
            time_zone__in=time_zone_filter).values().exclude(id__in=excluded_users_id).order_by('time_zone')
    else:
        model = Client.objects.filter(
            user=mailing_user,
            time_zone__in=time_zone_filter).values().exclude(id__in=excluded_users_id).order_by('-time_zone')
    model =list(model)
    for i in model:
        if end > timezone.now():
            # Creating a new message object
            new_message = Message.objects.create(status=0, mailing_id=mailing_id, client_id=int(i['id']))
            client_local_time = timezone.now() + timedelta(hours=int(i['time_zone']))
            new_message.save()
            if dt_start > client_local_time:
                send_message.apply_async([new_message.id, i['phone_number'], 'text'],
                                         eta=dt_start+timedelta(hours=int(i['time_zone']))
                                         )
            elif dt_end < client_local_time:
                new_message.status = 2
                new_message.save()
            else:
                response = send_message(id_message=new_message.id, phone=i['phone_number'], text=text)

                if response == 'OK':
                    new_message.status = 1
                    new_message.save()
                else:
                    new_message.status = 3
                    new_message.save()
                    model.append(i) # If the submission fails, the user is added to the end of the queue, to try again.
        else:
            break
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        mailing.active = False
        mailing.stopped = True
        mailing.save()
    except Exception as e:
        print(e)

# @app.task()

    # print(model)


# send_message(1, 79999999999, 'text')

# def nm():
#     pass