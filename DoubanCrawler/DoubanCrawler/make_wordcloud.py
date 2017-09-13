import re
import jieba
import pymysql
import matplotlib.pyplot as plt
from wordcloud import WordCloud


db = pymysql.connect(host='localhost',
    db='crawler',
    user='root',
    passwd='584224',
    charset='utf8',
    use_unicode=True)
cursor = db.cursor()

comments = {}
try:
    sql = 'select movie_id, comment_content from comments group by movie_id, comment_content'
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        movie_id, comment = row[0], row[1]
        if movie_id in comments.keys():
            comments[movie_id].append(comment)
        else:
            comments[movie_id] = list()
except Exception as e:
    print('Exception!')
    print(e)
finally:
    db.close()

import re
import jieba
import pymysql
import matplotlib.pyplot as plt
from wordcloud import WordCloud


db = pymysql.connect(host='localhost',
    db='crawler',
    user='root',
    passwd='584224',
    charset='utf8',
    use_unicode=True)
cursor = db.cursor()

comments = {}
try:
    sql = 'select movie_id, comment_content from comments group by movie_id, comment_content'
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        movie_id, comment = row[0], row[1]
        if movie_id in comments.keys():
            comments[movie_id].append(comment)
        else:
            comments[movie_id] = list()
except Exception as e:
    print('Exception!')
    print(e)
finally:
    db.close()

with open('/home/xuzuoyang/stopwords.txt') as file:
    stopwords = file.read().split('\n')

for movie_id in comments.keys():
    comment = ''.join(comments[movie_id])
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comment)
    cleaned_comment = ''.join(filterdata)

#     jieba.analyse.set_stop_words('/home/xuzuoyang/stopwords.txt')
#     tags=jieba.analyse.extract_tags(cleaned_comment, topK = 50, withWeight = False, allowPOS = ())
#     if stopwords:
#         words = [word for word in jieba.cut(cleaned_comment) if word not in stopwords]
#     else:
#         words = [word in jieba.cut(cleaned_comment)]
    words = jieba.cut(cleaned_comment)

    wordcloud = WordCloud('/home/xuzuoyang/Downloads/simsun.ttf', stopwords=stopwords).generate(' '.join(words))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
