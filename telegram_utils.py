import telegram
import requests

def send_telegram(photo_path="alert.png"):
    try:
        TOKEN = "6817143058:AAE_kD8EBpYDNonE5Y7qoVS-F3T2ozYn6YY"
        chat_id = "7283876279"
        url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
        files = {'photo': open(photo_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': 'trom kia bao cong an di'}

        response = requests.post(url, files=files, data=data)

        print(response.json())
    except Exception as ex:
        print("Can not send message telegram ", ex)

    print("Send success")