import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
import sys

def analyze(handle):
  twitter_consumer_key = ''
  twitter_consumer_secret = ''
  twitter_access_token = ''
  twitter_access_secret = ''

  twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret,
  access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=True)
  text = ""

  for status in statuses:
      if(status.lang == 'en'):
          text += status.text.encode('utf-8')

  pi_username = 'd637f6e3-f7a3-404f-a7ef-229a9e7d345b'
  pi_password = 'hZJEH0tirVfd'

  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
  pi_result = personality_insights.profile(text)
  return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data

def compare(r1, r2):
    compared_data = {}
    for keys in r1:
        compared_data[keys] = abs(r1[keys] - r2[keys])
    return compared_data

user1_handle = sys.argv[1]
user2_handle = sys.argv[2]

user1_result = analyze(user1_handle)
user2_result = analyze(user2_handle)
user1 = flatten(user1_result)
user2 = flatten(user2_result)

compared_results = compare(user1, user2)
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))
for keys, value in sorted_result[:5]:
    print keys,
    print(user1[keys]),
    print ('->'),
    print (user2[keys])
