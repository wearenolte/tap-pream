import requests
from datetime import datetime

from requests.exceptions import RequestException

from celery_app import app

from secret import access_token


fb_graph_url = "https://graph.facebook.com/v4.0/"
ig_business_id = "17841401743760151"


class Client:

    def __init__(self):
        self.session = requests.Session()


http_client = Client()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, name="instagram.get_user_metadata")
def get_user_metadata(ig_id):
    """
    Get Instagram user metadata
    :param ig_id: Instagram user id
    :return: Follower and media count of user
    """
    url = fb_graph_url + ig_id
    params = {
        "access_token": access_token,
        "fields": "followers_count,media_count"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return http_client.session.send(r.prepare()).json()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, name="instagram.get_user_insights")
def get_user_insights(ig_id):
    """
    Get Instagram user insights
    :param ig_id: Instagram user id
    :return: Insight metrics of a user
    """
    url = fb_graph_url + ig_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "audience_gender_age",
        "period": "lifetime"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return http_client.session.send(r.prepare()).json()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, name="instagram.get_user_medias")
def get_user_medias(ig_id):
    """
    Get media objects of a user
    """
    url = fb_graph_url + ig_id + "/media"
    params = {
        "access_token": access_token,
    }
    r = requests.Request(method='GET', url=url, params=params)
    return http_client.session.send(r.prepare()).json()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, name="instagram.get_media_metadata")
def get_media_metadata(ig_media_id):
    """
    Get metadata of an Instagram Media Object.
    """
    url = fb_graph_url + ig_media_id
    params = {
        "access_token": access_token,
        "fields": "caption,comments_count,like_count,media_type"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return http_client.session.send(r.prepare()).json()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, name="instagram.get_media_insights")
def get_media_insights(ig_media_id):
    """
    Get insights of an Instagram Media Object.
    """
    url = fb_graph_url + ig_media_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "engagement,impressions,reach"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return http_client.session.send(r.prepare()).json()


@app.task
def send_data(data):
    """Send fetched data to Stitch"""
    pass
# metadata = get_ig_user_metadata(ig_business_id)
# insights = get_ig_user_insights(ig_business_id)
# media_objects = get_ig_user_medias(ig_business_id)
# media_metadata = get_ig_media_metadata(media_objects['data'][1]['id'])
# media_insights = get_ig_media_insights(media_objects['data'][1]['id'])
# print("metadata: ", "\n", metadata)
# print("insights: ", "\n", insights)
# print("media objects: ", "\n", media_objects)
# print("media metadata :", "\n", media_metadata)
# print("media insights :", "\n", media_insights)

@app.task
def test_task():
    print(datetime.now())




