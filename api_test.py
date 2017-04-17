# import requests
#
# data = requests.get('http://localhost:8000/api/products?catname=Acc')
# print(data.json())
# print()
# data2 = requests.get('http://localhost:8000/api/products?name=viO&min=60&catname=string')
# print(data2.json())
# print()
# data3 = requests.get('http://localhost:8000/api/products?name=recorder&min=60&catname=string')
# print(data3)
# print()
# data4 = requests.get('http://localhost:8000/api/products?name=guitar&min=100&max=400')
# print(data4.json())

import stripe

stripe.api_key = 'sk_test_Xty8ov65XGF9KogaNpqEnbKL'
stripe.Charge.create(
  amount=2000,
  currency="usd",
  source="tok_19zWFwHiNrMfNGwJzh6Vk8oX", # obtained with Stripe.js
  description="Charge for ethan.taylor@example.com"
)
