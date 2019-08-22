import requests

access_token: "EAAGvXsNlQlQBAPrFpU59AXKAUyOUlUnYHdmS9XItpZAhdobTcqmQ6DnB9iuCY759auJOfr3jjrZA1s7mFaBf7FKpVg8K5CuwCYPaTXZA82ZAZBzXZBcQFwdiS6wmc47Xq5254dMvMxfZAG3QR6XShK7kyEndfZA8n7VKUb7zYZAm8BAZDZD"


fb_graph_url = "https://graph.facebook.com/v4.0/"
ig_business_id = "17841401743760151"

session = requests.Session()

import sys

print(sys.path)

class Client:
    def __init__(self):
        self.session = requests.Session()


def get_ig_user_metadata(ig_id):
    url = fb_graph_url + ig_id
    params = {
        "access_token": access_token,
        "fields": "followers_count,media_count"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare()).json()


def get_ig_user_lifetime_insights(ig_id):
    url = fb_graph_url + ig_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "audience_gender_age",
        "period": "lifetime"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare()).json()


def get_ig_user_medias(ig_id):
    url = fb_graph_url + ig_id + "/media"
    params = {
        "access_token": access_token,
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare()).json()


def get_ig_media_metadata(ig_media_id):
    url = fb_graph_url + ig_media_id
    params = {
        "access_token": access_token,
        "fields": "caption,comments_count,like_count,media_type"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare()).json()


def get_ig_media_insights(ig_media_id):
    url = fb_graph_url + ig_media_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "engagement,impressions,reach"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare()).json()


metadata = get_ig_user_metadata(ig_business_id)
insights = get_ig_user_lifetime_insights(ig_business_id)
media_objects = get_ig_user_medias(ig_business_id)
media_metadata = get_ig_media_metadata(media_objects['data'][1]['id'])
media_insights = get_ig_media_insights(media_objects['data'][1]['id'])
print("metadata: ", "\n", metadata)
print("insights: ", "\n", insights)
print("media objects: ", "\n", media_objects)
print("media metadata :", "\n", media_metadata)
print("media insights :", "\n", media_insights)



