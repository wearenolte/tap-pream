import requests
from requests.exceptions import RequestException
from datetime import datetime, timezone

from celery import chord, group
from requests.exceptions import RequestException, Timeout

from celery_app import app
from secret import access_token


fb_graph_url = "https://graph.facebook.com/v4.0/"
ig_business_ids = ["17841401743760151"]


def add_timestamp(data):
    now = datetime.now(timezone.utc)
    data['server_time'] = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    return data


@app.task(max_retries=3, retry_backoff=1, name="instagram.get-user-metadata")
def get_user_metadata(ig_id):
    """
    Get Instagram user metadata
    """
    url = fb_graph_url + ig_id
    params = {
        "access_token": access_token,
        "fields": "id,ig_id,followers_count,media_count"
    }

    r = requests.get(url=url, params=params)
    if not r.ok:
        if r.status_code == 400:
            # TODO: log 400 error
            raise
        else:
            raise get_user_metadata.retry()
    data = r.json()
    data = add_timestamp(data)
    return data


@app.task(max_retries=3, retry_backoff=1, name="instagram.get-user-medias")
def get_user_medias(ig_id):
    """
    Get media objects of Instagram user
    """
    url = fb_graph_url + ig_id + "/media"
    params = {
        "access_token": access_token,
    }
    r = requests.get(url=url, params=params)
    if not r.ok:
        if r.status_code == 400:
            # TODO: log 400 error
            raise
        else:
            raise get_user_metadata.retry()
    data = r.json()
    data = add_timestamp(data)
    return data


@app.task(max_retries=3, retry_backoff=1, name="instagram.get-post-metadata")
def get_post_metadata(ig_media_id):
    """
    Get metadata of an Instagram media object
    """
    url = fb_graph_url + ig_media_id
    params = {
        "access_token": access_token,
        "fields": "id,_ig_id,caption,comments_count,like_count,media_type"
    }
    r = requests.get(url=url, params=params)
    if not r.ok:
        if r.status_code == 400:
            # TODO: log 400 error
            raise
        else:
            raise get_user_metadata.retry()
    data = r.json()
    data = add_timestamp(data)
    return data


@app.task(max_retries=3, retry_backoff=1, name="instagram.get-post-insights")
def get_post_insights(ig_media_id):
    """
    Get insights of an Instagram media object
    """
    url = fb_graph_url + ig_media_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "engagement,impressions,reach"
    }
    r = requests.get(url=url, params=params)
    if not r.ok:
        if r.status_code == 400:
            # TODO: log 400 error
            raise
        else:
            raise get_user_metadata.retry()
    data = r.json()
    data = add_timestamp(data)
    return data


@app.task(name="instagram.target-stitch")
def target_stitch(data, table_name):
    """
    Send data to Stitch Import API
    Max 4 MB or 10.000 data points
    """
    pass


@app.task(name="instagram.update_user_metadata")
def update_user_data():
    """
    Celery chords to poll user data from IG Graph API and send to Stitch API
    Fetches user ids from Pream API and starts a task chain
    Logs partial and total execution times on Sentry
    """
    user_ids = []  # TODO: fetch user_ids
    metadata = chord(group(get_user_metadata.s(user_id) for user_id in user_ids), target_stitch.s("user_metadata"))
    metadata.apply_async()


@app.task(name="instagram.update_post_data")
def update_post_data():
    post_ids = []
    metadata = chord(group(get_post_metadata.s(post_id) for post_id in post_ids), target_stitch.s("post_metadata"))
    insights = chord(group(get_post_insights.s(post_id) for post_id in post_ids), target_stitch.s("post_insights"))
    group(metadata, insights).apply_async()


@app.task(autoretry_for=(RequestException,), retry_backoff=1)
def test_request_fail():
    try:
        raise RequestException
    except RequestException as e:
        print('Try {0}/{1}'.format(test_request_fail.request.retries, test_request_fail.max_retries))
        # Print log message with current retry
        raise


@app.task
def test_task_send(a_list):
    return f"a list: {a_list}"


@app.task
def test_task_get_data(d):
    return "user: " + d


@app.task
def test_task_flow():
    user_ids_1 = ["1", "2", "3", "4", "5"]
    user_ids_2 = ["10", "11", "12", "13", "14"]
    task_flow_1 = chord(group(test_task_get_data.s(user_id) for user_id in user_ids_1), test_task_send.s())
    task_flow_2 = chord(group(test_task_get_data.s(user_id) for user_id in user_ids_2), test_task_send.s())
    tasks = group(task_flow_1, task_flow_2).apply_async()
    return tasks






