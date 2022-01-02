#!/bin/bash

# Use your user credentials to login using the dj_rest_auth route for logging in
# /auth/login/ will depend on the URL set in urls.py
# Should expect a response in the format {"key":"generated_token_key"}


read -s -p "Email: " EMAIL
echo $EMAIL
read -s -p "Password: " PASSWORD

LOGIN_URL="http://127.0.0.1:8000/auth/login/"
get_login_json()
{
    cat <<EOF
{
    "username": "$EMAIL",
    "password": "$PASSWORD"
}
EOF
}

echo "Logging in at: $LOGIN_URL"

RESPONSE=$(curl --request POST \
      --url $LOGIN_URL \
      -H 'Content-Type: application/json' \
      --data "$(get_login_json)" )

echo "response: $RESPONSE"