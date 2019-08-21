import requests

access_token = "EAAGvXsNlQlQBAPrFpU59AXKAUyOUlUnYHdmS9XItpZAhdobTcqmQ6DnB9iuCY759auJOfr3jjrZA1s7mFaBf7FKpVg8K5CuwCYPaTXZA82ZAZBzXZBcQFwdiS6wmc47Xq5254dMvMxfZAG3QR6XShK7kyEndfZA8n7VKUb7zYZAm8BAZDZD"

fb_graph_url = "https://graph.facebook.com/v4.0/"
ig_business_id = "17841401743760151"

session = requests.Session()


def get_ig_user_metadata(ig_id):
    url = fb_graph_url + ig_id
    params = {
        "access_token": access_token,
        "fields": "followers_count,media_count"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare())


def get_ig_user_lifetime_insights(ig_id):
    url = fb_graph_url + ig_id + "/insights"
    params = {
        "access_token": access_token,
        "metric": "audience_gender_age",
        "period": "lifetime"
    }
    r = requests.Request(method='GET', url=url, params=params)
    return session.send(r.prepare())


def get_user_medias():
    pass


metadata = get_ig_user_metadata(ig_business_id)
insights = get_ig_user_lifetime_insights(ig_business_id)
print("metadata: ", "/n", metadata.json())
print("insights: ", "/n", insights.json())

