import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import string
from nltk import word_tokenize
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

keyword_input = 'Russia'
keyword = urllib.parse.quote(keyword_input)
print('Преобразование строки Russia в URL-код для поиска: ', keyword)

base_url = 'https://news.google.com'
search_url = base_url + '/search?q=' + keyword + '&hl=en-US&gl=US&ceid=US%3Aen'
print('URL-адреса в сочетании с поисковыми запросами:', search_url)

# прошлая дата
past_date = datetime.date.today() - datetime.timedelta(days=30)


def google_news_clipping_keyword(keyword_inp):
    keyword = urllib.parse.quote(keyword_inp)

    url = base_url + '/search?q=' + keyword + '&hl=en-US&gl=US&ceid=US%3Aen'

    resp = requests.get(url)
    html_src = resp.text
    soup = BeautifulSoup(html_src, 'lxml')

    news_items = soup.select('div[class="xrnccd"]')
    # print(news_items)

    titles = []

    for item in news_items:
        news_reporting = item.find('time', attrs={'class': 'WW6dff uQIVzc Sksgp'})
        news_reporting_datetime = news_reporting.get('datetime').split('T')
        news_reporting_date = news_reporting_datetime[0]
        dt = datetime.datetime.strptime(news_reporting_date, '%Y-%m-%d').date()
        if dt < past_date:
            continue

        news_title = item.find('a', attrs={'class': 'DY5T1d'}).getText()
        titles.append(news_title)

    result = titles

    return result


news = google_news_clipping_keyword(keyword_input)
# print(news)
# Записываем в файл все загоголовки новостей
MyFile = open('output.txt', 'w')
MyList = map(lambda x: x + '\n', news)
MyFile.writelines(MyList)
MyFile.close()

f = open('output.txt', "r", encoding="utf-8")
text = f.read()
# Получаем текст без символов пунктуации
text = "".join([ch for ch in text if ch not in string.punctuation])
# Получаем текст без цифр
text = "".join([ch for ch in text if ch not in string.digits])

# Разбиваем текст на слова
# Получаем токены
text_tokens = word_tokenize(text)
# print(text_tokens)
text = nltk.Text(text_tokens)

# Убираем стоп слова
english_stopwords = stopwords.words("english")
english_stopwords.extend(['Is', 'The', 'In', 'Its', 'You', ''])

# print(len(english_stopwords))
text_tokens = [token.strip() for token in text_tokens if token not in english_stopwords]
text = nltk.Text(text_tokens)

# Вычисляем 50 топ слов
fdist = FreqDist(text)
text = []
for key, num in fdist.most_common(50):
    text.append(key)
# Построение облака слов
text_raw = " ".join(text)
wordcloud = WordCloud().generate(text_raw)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
