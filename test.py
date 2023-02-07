from bs4 import BeautifulSoup
import requests

url = "https://www.zalando.pl/dr-martens-1460-unisex-botki-sznurowane-old-oxblood-do215k03a-g11.html"

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6"
    }

response = requests.get(url, headers=head)
web_page = response.content
soup = BeautifulSoup(web_page, "html.parser")

brand = soup.find_all(class_="SZKKsK mt1kvu FxZV-M pVrzNP _5Yd-hZ")
product = soup.find_all(class_="EKabf7 R_QwOV")
price = soup.find_all(class_="_0Qm8W1 uqkIZw FxZV-M pVrzNP")
if price == []:
    price = soup.find_all(class_="_0Qm8W1 uqkIZw dgII7d TQ5FLB")
    if price == []:
        price = soup.find_all(class_="_0Qm8W1 uqkIZw dgII7d TQ5FLB mx_ksa")
    print

x = price[0].getText().split("\\")
print(x[0])

