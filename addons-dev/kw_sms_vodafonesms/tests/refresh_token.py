import requests
import json

url = "https://a2p.vodafone.ua/uaa/oauth/token?grant_type=refresh_token&refresh_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJvbC1rb3R2eXRza3lpQGZvcndhcmQtYmFuay5jb20iLCJ1c2VyX2tleSI6IjQ0Y2MxNjIxLWMzMjktNGMzMS04Y2JlLWQxZmY1MWIwNWEzOSIsImFkZGl0aW9uYWxEZXRhaWxzIjp7ImN1c3RvbWVyX3Byb2ZpbGVfaWQiOiI0OTk3Njc0In0sImF1dGhvcml0aWVzIjpbIlJPTEVfT0JNX0NVU1RPTUVSX01BTkFHRVIiXSwiY2xpZW50X2lkIjoiaW50ZXJuYWwiLCJjcmVhdGVUb2tlblRpbWUiOjE2OTk2OTI5NzU1NDMsInNjb3BlIjpbIm9wZW5pZCJdLCJyb2xlX2tleSI6IlJPTEVfT0JNX0NVU1RPTUVSX01BTkFHRVIiLCJhdGkiOiIyMmU5MTYwNS1lMzVjLTQ1NGItYjQxOS0wYjVlMjZiYzk4Y2YiLCJleHAiOjE3MDIyODQ5NzUsImxvZ2lucyI6W3sidHlwZUtleSI6IkxPR0lOLk5JQ0tOQU1FIiwic3RhdGVLZXkiOm51bGwsImxvZ2luIjoi0LDQutGG0ZbQvtC90LXRgNC90LUg0YLQvtCy0LDRgNC40YHRgtCy0L4gXCLQsdCw0L3QuiDRhNC-0YDQstCw0YDQtFwiIn0seyJ0eXBlS2V5IjoiTE9HSU4uTVNJU0ROIiwic3RhdGVLZXkiOm51bGwsImxvZ2luIjoiMzgwNTAzMTA4Nzk1In0seyJ0eXBlS2V5IjoiTE9HSU4uRU1BSUwiLCJzdGF0ZUtleSI6bnVsbCwibG9naW4iOiJvbC1rb3R2eXRza3lpQGZvcndhcmQtYmFuay5jb20ifV0sImp0aSI6IjY2YjMxMzkyLTZkMmEtNDM2ZC1hNTE0LWIwYTkyM2RjNmZkYiIsInRlbmFudCI6IlhNIn0.KhPYgo35D2O7S_ouv1un6TW71TKOu_csYjbzk_WMYgXE5DiKzrLT35mIbPFPETsyQ8zh9QJNIpNHrZK-XY3F8fItJjB5v0Gw7J4wnXzkFoogx3xSM3BxLCiEloXzcYc99-FDEGa3dx921PN6jZx7BzwsGMQTL5Jv5xdP8K5Y61fTB765MTwUgwNBZO5Pywg_SoDvhg1nLMhcve4WTlQ4Nzk-xW-XTPECJbDCIspsDP9qC9GbVbxP8ISRfh78oU-uas1LnqWsH6EzzZdN91mPliNl4n4yVQBOnAO45n1Foo7wereaxdUUNNmd5M59wO82Rvp5_w3rygNrNaE5CVkErw"

payload = {}
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic aW50ZXJuYWw6aW50ZXJuYWw=',
  'Cookie': 'BIGipServerSF-OBM-30000=3500872876.12405.0000; TS01ee2dd3=01289bfb4ab5022a6f3d9df614ca37977750bfc3c88a9cd1bc36bccfde3c09fc94c2bc5fb37c7bbea0f6db6340db86757c2fcea6c6'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
