import requests
from datetime import datetime


def send_post_request():
    request_data = {
        'url': 'https://www.dtek-dnem.com.ua/ua/ajax',
        'headers': {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'priority': 'u=1, i',
            'sec-ch-ua': '\'Not/A)Brand\';v=\'8\', \'Chromium\';v=\'126\', \'Opera GX\';v=\'112\'',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '\'Windows\'',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-csrf-token': 'OXsYjtIDbw6sgsQIrVbN9kD2Wn2zr6wzUypCI1QS6wlTOSC2gmclaMXKtWf0Ea-AbZQ3GYbo-AYFGHFHAXbGZw==',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'Domain=dtek-dnem.com.ua; _language=1c65c25ab698cb454bcc1ea3dd198f11906b9a05154d60231a781543ab2d12f3a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_language%22%3Bi%3A1%3Bs%3A2%3A%22uk%22%3B%7D; _csrf-dtek-dnem=544718c0051ba6834f7cf6016a1c0983911946f053afce5b56a2cef388f87e55a%3A2%3A%7Bi%3A0%3Bs%3A15%3A%22_csrf-dtek-dnem%22%3Bi%3A1%3Bs%3A32%3A%22jB88PdJfiHqoYGbv-bmd5GT5V23dUd-n%22%3B%7D; visid_incap_2224656=lOvpFSYXQqilQFK9T5asGhzee2YAAAAAQUIPAAAAAAAqTEsGawkdsgQCXZVD0F3Z; _gid=GA1.3.1232207805.1724742643; Domain=dtek-dnem.com.ua; incap_ses_766_2224656=pdNfaS/ZECZjLpQA/WChCmnezWYAAAAAOTUIYxNldkdrVSvXUuB/0w==; dtek-dnem=833pvrrhmdrs6n4hjsfe15g888; incap_ses_1688_2224656=k5e7DwWH6DArVYv+FftsFwfuzmYAAAAA54EdQirTOoeXEuCC/IX5mQ==; _gat_gtag_UA_98999031_3=1; _ga_HN94V8NN5L=GS1.1.1724837384.113.1.1724837402.42.0.0; _ga=GA1.3.1000927330.1719393823; incap_wrt_376=Hu7OZgAAAADCrS9hGQAI+AIQjv+NuC4Yyt67tgYgAiiG3Lu2BjAB3MPrkY4rRD8jp2YFTBwb4w==',
            'Referer': 'https://www.dtek-dnem.com.ua/ua/shutdowns',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        },
        'body': {
            'method': 'getHomeNum',
            'data[0][name]': 'city',
            'data[0][value]': 'м. Дніпро',
            'data[1][name]': 'street',
            'data[1][value]': 'вул. Десантна'
        }
    }

    try:
        response = requests.post(
            request_data['url'],
            headers=request_data['headers'],
            data=request_data['body']
        )
        response.raise_for_status()  # Проверка на успешный ответ
        return response.json()
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None


def format_remaining_time(remaining_time):
    days, seconds = remaining_time.days, remaining_time.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours} hours, {minutes} minutes, {seconds} seconds'


def process_outage_info(data):
    outage_13 = data['data'].get('13', {})

    sub_type = outage_13.get('sub_type', '')
    start_date = outage_13.get('start_date', '')
    end_date = outage_13.get('end_date', '')

    if not sub_type and not start_date and not end_date:
        print('Light is present')
    else:
        try:
            end_datetime = datetime.strptime(end_date, '%H:%M %d.%m.%Y')
            current_datetime = datetime.now()
            remaining_time = end_datetime - current_datetime
            time_remaining_str = format_remaining_time(remaining_time)

            print(f'Light is absent in 13 house:')
            print(f'Type: {sub_type}')
            print(f'Start time: {start_date}')
            print(f'End time: {end_date}')
            print(f'Time left: {time_remaining_str}')
        except ValueError as e:
            print(f"Error parsing date: {e}")


def main():
    response_data = send_post_request()
    if response_data:
        process_outage_info(response_data)


if __name__ == "__main__":
    main()

input()
