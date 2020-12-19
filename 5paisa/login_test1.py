import requests

s = requests.Session()
headers = {
    'authority': 'www.5paisa.com',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.5paisa.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.5paisa.com/',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': '_gcl_au=1.1.1694663341.1600523099; utm_campaign_cookie_eaccount=; _fbp=fb.1.1600523099995.498828509; utm_campaign_cookie=; PIData=U09VUkFW; WZRK_G=92feefdd4fa24231a498161f481a5600; source=www.google.com|mail.google.com|mail.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|github.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com|www.google.com; _ga_0ZW7K75KJP=GS1.1.1603524384.36.0.1603524384.0; gclid=undefined; _ga=GA1.2.1280417679.1600523099; _gid=GA1.2.575694897.1606587289; __RequestVerificationToken=HiYhpm6ej1orEweQHTGJHK6eQicw-xNHxfIIclBbmsMltcXzGPiup5In3AcYvSBuidbf0G9buqYG4bKFzAqm7d0qzxA1; RClient=; 5paisacookie=yoo1vf4kavgmedlzyot4zrtz; WZRK_S_675-RZ7-6Z5Z=%7B%22p%22%3A2%2C%22s%22%3A1606717821%2C%22t%22%3A1606718904%7D; ASP.NET_SessionId=j40ph2dnycbx2kghyev3gvnd; WZRK_S_R74-5R4-6W5Z=%7B%22p%22%3A11%2C%22s%22%3A1606717796%2C%22t%22%3A1606719087%7D',
}

response = s.get('https://www.5paisa.com/', headers=headers)

print(response)
# print(response.text.encode('utf8'))
print(s.cookies.get_dict())


data = {
  'Email': 'srvz39@gmail.com'
}

response = s.post('https://www.5paisa.com/home/checkclient', data=data)

print(response)
print(response.text.encode('utf8'))
print(s.cookies.get_dict())

data = {
  'login.UserName': 'srvz39@gmail.com',
  'login.ClientCode': '',
  'login.Password': '151220205p!',
  'login.DOB': '27051990'
}

response = s.post('https://www.5paisa.com/Home/Login', headers=headers, data=data)

print(response)
print(response.text.encode('utf8'))
print(s.cookies.get_dict())