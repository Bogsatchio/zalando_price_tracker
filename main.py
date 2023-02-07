from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from sqlalchemy import create_engine
import pyodbc
from datetime import datetime

# making a Soup with requests
url1 = "https://www.zalando.pl/dr-martens-1460-unisex-botki-sznurowane-old-oxblood-do215k03a-g11.html" # Martensy
url2 = "https://www.zalando.pl/timberland-6-inch-premium-botki-i-ankle-boots-brazowy-ti112c04a-702.html" # Timberlandy
url3 = "https://www.zalando.pl/adidas-originals-stripes-pant-spodnie-treningowe-black-ad1210011-q11.html" # dresy Adidas
url4 = "https://www.zalando.pl/tom-tailor-denim-koszula-original-to722d0eq-k11.html" # Koszula
url5 = "https://www.zalando.pl/napapijri-t-shirt-basic-blu-marine-na622o066-k11.html" # T-shirt Napap
url6 = "https://www.zalando.pl/gap-arch-bluza-z-kapturem-navy-gp022s078-k11.html" # Bluza GAP
url7 = "https://www.zalando.pl/adidas-originals-logo-bluza-z-kapturem-black-ad122s0mm-q11.html" #bluza Adidas
url8 = "https://www.zalando.pl/adidas-originals-szorty-black-ad121s05x-q11.html" # Szorty Damskie Adidas
url9 = "https://www.zalando.pl/adidas-originals-kurtka-przejsciowa-black-ad12100b6-q11.html" # Kurtka Adidas
url10 = "https://www.zalando.pl/gap-tee-t-shirt-z-nadrukiem-gp021d0cd-k11.html" #Damski Tshirt GAP
url11 = "https://www.zalando.pl/timberland-ss-dunstan-river-crew-tee-t-shirt-basic-balsam-green-ti122o02r-m11.html" # Thsirt Timberland
url12 = "https://www.zalando.pl/timberland-bluza-z-polaru-black-ti121i002-q11.html" # Polar Timberland
url13 = "https://www.zalando.pl/tom-tailor-denim-koszula-white-to722d0eq-a11.html" #koszula 2
url14 = "https://www.zalando.pl/napapijri-droz-sweter-black-041-na622q02y-q11.html" #sweter Napap
url15 = "https://www.zalando.pl/napapijri-bluza-black-na622s06k-q11.html" # Bluza Napap

urls = [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11, url12, url13, url14, url15]

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6"
#    "Cookie": "PHPSESSID=5ipso0ilc540fc1jn9i1af81s6; _ga=GA1.2.817988229.1672299907; _gid=GA1.2.45897261.1672299907"
}


l_brands = []
l_products = []
l_price = []
for x in urls:
    #1. Making Soup
    response = requests.get(x, headers=head)
    web_page = response.content
    soup = BeautifulSoup(web_page, "html.parser")

    #2. Extracting Brand Name, Product Name and Price
    brand = soup.find_all(class_="SZKKsK mt1kvu FxZV-M pVrzNP _5Yd-hZ")
    product = soup.find_all(class_="EKabf7 R_QwOV")
    price = soup.find_all(class_="_0Qm8W1 uqkIZw FxZV-M pVrzNP")
    if price == []:
        price = soup.find_all(class_="_0Qm8W1 uqkIZw dgII7d TQ5FLB") # klasa ceny na wyprzedarzy
        if price == []:
            price = soup.find_all(class_="_0Qm8W1 uqkIZw dgII7d TQ5FLB mx_ksa")
    l_brands.append(brand[0].getText())
    l_products.append(product[0].getText())

    price_splt = price[0].getText().split("\\")[0]
    #print(price_clean)
    price_clean = float(re.sub("[ł]","",(re.sub("[a-z]", "", price_splt))).strip().replace(",", "."))
    print(price_clean)
    l_price.append(price_clean)
    # print(brand[0].getText())
    # print(product[0].getText())
    # print(price[0].getText())
print(l_brands)
print(l_products)
print(l_price)

# create dataframe out of lists
df = pd.DataFrame(list(zip(l_brands, l_products, l_price)), columns=["Brand", "Product", "Price"])
today = datetime.today().strftime('%Y-%m-%d')
df.insert(loc=0, column="Date", value=today, allow_duplicates=True)
# connecting to the Database

svr_name = "LAPTOP-TJOJR8JH"
db_name = "test"
driver = "ODBC Driver 17 for SQL Server"
db_con = f"mssql://@{svr_name}/{db_name}?driver={driver}"

eng = create_engine(db_con)
connection = eng.connect()
print(df)

df.to_sql("Zalando_DB", con=eng, if_exists="append", index=False)
print(df)