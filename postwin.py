import requests

url = 'http://127.0.0.1:5000/add/winery'
myobj = {
    'winery_id': 1,
    'winery_lat': 44.52820,
    'winery_long': 10.92102
}
print(myobj)
x = requests.post(url, data=myobj)
print(x)
print(x.text)

myobj2 = {
    'winery_id': 2,
    'winery_lat': 44.50462842959038,
    'winery_long': 10.923375979946016
}
print(myobj2)
x2 = requests.post(url, data=myobj2)
print(x2)
print(x2.text)

myobj3 = {
    'winery_id': 3,
    'winery_lat': 44.50342955149953,
    'winery_long': 11.086431198448272
}
print(myobj3)
x3 = requests.post(url, data=myobj3)
print(x3)
print(x3.text)



