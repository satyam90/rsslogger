# scraping.py
import requests
import xlsxwriter
from bs4 import BeautifulSoup

# initializers
all_articles = [['Title', 'Description', 'Comments',
                 'Published', 'Link', 'Duration', 'Summary', 'Sub Title']]
workbook = xlsxwriter.Workbook('rss.xlsx')
worksheet = workbook.add_worksheet()
row = 0

# scraping function


def readFile(url):
    response = requests.get(url).text
    lines = response.splitlines()

    for line in lines:
        hackernews_rss(line)


def hackernews_rss(url):
    # print('Extracting: ', url)
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        for a in articles:
            article = [
                a.find('title').text,
                a.find('description').text,
                a.find('comments').text,
                a.find('pubDate').text,
                a.find('link').text,
                a.find('itunes:duration').text,
                a.find('itunes:summary').text,
                a.find('itunes:subtitle').text
            ]

            all_articles.append(article)

        print(len(all_articles))
        writeToFile()
    except Exception as e:
        print('Failed to extract URL: ', url, '###', e)
        print('')


def writeToFile():
    global row
    for article in all_articles:
        column = 0
        for item in article:
            worksheet.write(row, column, item)
            column += 1
        row += 1
    all_articles.clear()


# hackernews_rss("https://news.ycombinator.com/rss")
readFile('https://gist.githubusercontent.com/eteubert/5986525/raw/a225d0db5c8c287972c4671f99af007b72b94ce2/feeds_unique.txt')
workbook.close()
print('Finished scraping')
