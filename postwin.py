import requests

url = 'http://127.0.0.1:5000/add/winery'
myobj = {
    'winery_id': 0,
    'winery_location': 'test'
}
print(myobj)
x = requests.post(url, data=myobj)
print(x)
print(x.text)

myobj2 = {
    'winery_id': 1,
    'winery_location': 'test2'
}
print(myobj2)
x2 = requests.post(url, data=myobj2)
print(x2)
print(x2.text)

myobj3 = {
    'winery_id': 2,
    'winery_location': 'test3'
}
print(myobj3)
x3 = requests.post(url, data=myobj3)
print(x3)
print(x3.text)
