#!/bin/bash

# Using the credentials obtains from dj_rest_login.sh
# Access the /stub/ endpoint

read -s -p "Access token: " ACCESS_TOKEN
echo $ACCESS_TOKEN

STUB_URL="http://127.0.0.1:8000/stub/"

echo "Accessing data at: $STUB_URL with token $ACCESS_TOKEN"

RESPONSE=$(curl --request GET \
      --url $STUB_URL \
      -H "Authorization: Token $ACCESS_TOKEN" )

echo "response: $RESPONSE"