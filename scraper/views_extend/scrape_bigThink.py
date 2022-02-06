from bs4 import BeautifulSoup
import requests
import shutil

from PIL import Image

import shutil


html_text = requests.get('https://bigthink.com/thinking/').text
soup = BeautifulSoup(html_text, 'lxml')
articles = soup.find_all('div', class_ = 'card-content')



def scrape_bigThink_funct():

    n = 1
    news = []

    for article in articles:

        if article.find('a'):
            name = article.find_all('a')
            for i in range (0, 2):
                if i == 1:
                    info = name[i]['href']
                    news.append({'title':name[i].text, 'info': info, 'image': f'static/bigThink/image{n}.jpg'})
                    n += 1

        if article.find('div', class_ = 'card-excerpt'):
            perex = article.find('div', class_ = 'card-excerpt').text.replace('  ', '')
            news[len(news)-1]['perex'] = perex


    n = 0
    # Find and download image
    articles_imgages = soup.find_all('article')
    for image in articles_imgages:
        if n > 0:
            img = image.find('img')
            img = img['src']

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
                    new_image.append((255, 243, 55))
                else:
                    new_image.append((0,207,79))

                    
            # update image data
            img.putdata(new_image)


            img.save(f"image{n}.jpg")

            shutil.move(f'image{n}.jpg', f'scraper/static/bigThink/image{n}.jpg')
        n += 1

    return news
