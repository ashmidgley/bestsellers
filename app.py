from flask import Flask, render_template
import requests
import bs4

app = Flask(__name__)

class Bestseller:
    def __init__(self, title, author, price):
        self.title = title
        self.price = price
        self.author = author

@app.route('/')
def index():
    bestsellers = get_bestsellers()
    headers = getRequestHeaders()
    return render_template("index.html", bestsellers=bestsellers, headers=headers)

def getRequestHeaders():
    res = requests.get('https://www.bookdepository.com/')
    print(res.headers)
    return res.headers.values()

def get_bestsellers():
    res = requests.get('https://www.bookdepository.com/')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    bestsellers = []
    for i in soup.select('.tab-373 > .tab > .book-item > .item-info'):
        title = i.select('.title > a')[0].text.replace(",", "").strip()
        author = i.select('.author > span > a > span')[0].text.strip()
        price = 'Unavailable'
        if(i.select('.price-wrap > .price')):
            price = i.select('.price-wrap > .price')[0].text.strip().split(' ')[0]
            bs = Bestseller(title, author, price)
            bestsellers.append(bs)
    return bestsellers

if __name__ == "__main__":
    app.run(debug=True)
