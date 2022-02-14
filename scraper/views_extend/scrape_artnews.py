# web scraping libraries
from bs4 import BeautifulSoup
import requests

# Image procesing
from PIL import Image
import shutil


def scrape_artnews_funct():
    # Artnews
    news = []

    # Addres
    html_text = requests.get('https://www.artnews.com/c/art-news/news/').text
    soup = BeautifulSoup(html_text, 'lxml')
    articles = soup.find_all('article')

    for n, article in enumerate(articles):

        if article.find('a', class_ = 'c-title__link'):
            name = article.find('a', class_ = 'c-title__link').text.replace('  ', '')
            info = article.a['href']

            # Find and download image
            img = article.find('img', class_ = 'c-lazy-image__img')
            img = img['data-lazy-src']

            res = requests.get(img, stream = True)
            file_name = f'image{n}.jpg'

            # Download image
            if res.status_code == 200:
                with open(file_name,'wb') as f:
                    shutil.copyfileobj(res.raw, f) 
                print('Image sucessfully Downloaded: ',file_name)
            else:
                print('Image Couldn\'t be retrieved')

            # Make image black and white
            file = f"image{n}.jpg"

            img = Image.open(file)
            img = img.convert("1")
            img = img.convert("RGB")
            d = img.getdata()
            new_image = []
            for item in d:
            
                # change all white (also shades of whites)
                # pixels to yellow
                if item[0] in list(range(200, 256)):
                    new_image.append((255,171,193))
                else:
                    new_image.append((100, 99, 139))
                    
            # update image data
            img.putdata(new_image)


            img.save(f"image{n}.jpg")

            shutil.move(f'image{n}.jpg', f'scraper/static/artnews/image{n}.jpg')

            news.append({'title':name.strip(), 'info': info, 'image': f'static/artnews/image{n}.jpg'})



        if article.find('p', class_ = 'c-dek'):
            perex = article.find('p', class_ = 'c-dek').text.replace('  ', '')
            news[len(news)-1]['perex'] = perex.strip()

    return news