import requests

from_num = "949-636-2053"
messId = "4"
body = "google maps los angeles, san francisco"
payload = {"From":from_num, "MessageSid":messId, "Body":body}
conn = requests.get("http://127.0.0.1:5001/twilio", params=payload)
