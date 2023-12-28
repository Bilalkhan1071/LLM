import json
import requests
import html  # Import the html module for unescaping

#ENTER YOUR PROMPT BELOW
userprompt = "What does the article talk about, explain to me as if i am a professional in the field"

#LAMBDA SETUP WITH JSON RESPONSE
url = "https://ozlrtotpqg.execute-api.us-east-2.amazonaws.com/myStage/query"
headers = {"content-type": "application/json"}
payload = json.dumps(
    {
        "resource": "/query",
        "path": "/query",
        "httpMethod": "POST",
        "requestContext": {},
        "multiValueQueryStringParameters": None,
        "body": json.dumps({"userprompt": userprompt})  # Include userprompt in the JSON body
    }
)

response = requests.post(url=url, headers=headers, data=payload)

#PARSE JSON TO GET CLEAN OUTPUT
results_json = response.json().get('body', None)
if not results_json:
    print("Application timed out while lambda was warming up. Please run command again!")
results_dict = json.loads(results_json)
output = results_dict['result']

print(output)
