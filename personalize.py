import boto3

import json
import numpy as np
import pandas as pd
import time

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')



data = pd.read_csv('./playstore-user-interaction-data-10k.csv', sep=',', names=['USER_ID', 'ITEM_ID', 'TIMESTAMP'])
pd.set_option('display.max_rows', 5)
data

items = pd.read_csv('./playstore_unique_816.csv', sep=',', usecols=[0,1], encoding='latin-1')
items.columns = ['ITEM_ID', 'TITLE']

user_id, item_id, _ = data.sample().values[0]
#item_title = items.loc[items['ITEM_ID'] == item_id].values[0][-1]
print("USER: {}".format(user_id))
print("ITEM: {}".format(item_id))

items

get_recommendations_response = personalize_runtime.get_recommendations(
    #campaignArn = campaign_arn,
    #userId = str(user_id),
    #itemId = str(item_id),
    campaignArn = "arn:aws:personalize:us-east-1:660036929150:campaign/aws-playstore-campaign",
    userId = "80",
    itemId = "201"
)

item_list = get_recommendations_response['itemList']
title_list = [items.loc[items['ITEM_ID'] == np.int(item['itemId'])].values[0][-1] for item in item_list]

print("Recommendations: {}".format(json.dumps(title_list, indent=2)))

