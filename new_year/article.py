from pages.application.activity.new_year.db import (
    get_articles, get_article_by_id, get_articles_by_user, get_prises, insert_article, delete_article, update_article
)
from pages.application.activity.new_year.feature import article_comment_amount
from pages.application.activity.new_year.user import get_user_info_from_database


def get_all_articles():
    all_article = []
    for data in get_articles():
        all_article.append({
            'article_id': data[0],
            'user': get_user_info_from_database(data[1]),
            'title': data[2],
            'content': data[3] if len(data[3]) <= 200 else data[3][:200],
            'date': data[4],
            'prises': len(get_prises(data[0])),
            'comments': article_comment_amount(data[0])
        })
    articles_quick_sort(all_article)
    return all_article


def articles_quick_sort(all_article):
    def quick_sort(articles, left, right):
        if left < right:
            pivot_index = partition(articles, left, right)
            quick_sort(articles, left, pivot_index - 1)
            quick_sort(articles, pivot_index + 1, right)

    def partition(articles, left, right):
        pivot_value = articles[right]['prises'] + articles[right]['comments']
        pivot_index = left - 1
        for index in range(left, right):
            if articles[index]['prises'] + articles[index]['comments'] >= pivot_value:
                pivot_index += 1
                articles[pivot_index], articles[index] = articles[index], articles[pivot_index]
        articles[pivot_index + 1], articles[right] = articles[right], articles[pivot_index + 1]
        return pivot_index + 1

    quick_sort(all_article, 0, len(all_article)-1)


def user_articles(yb_id):
    datas = get_articles_by_user(yb_id)
    if datas == ():
        return None
    articles = []
    for data in datas:
        articles.append({
            'article_id': data[0],
            'user': get_user_info_from_database(data[1]),
            'title': data[2],
            'content': data[3] if len(data[3]) <= 200 else data[3][:200],
            'date': data[4],
            'prises': len(get_prises(data[0])),
            'comments': article_comment_amount(data[0])
        })
    return articles


def get_article(article_id):
    data = get_article_by_id(article_id)
    if data is None:
        return None
    article = {
        'article_id': data[0],
        'user': get_user_info_from_database(data[1]),
        'title': data[2],
        'content': data[3],
        'date': data[4]
    }
    return article


def article_submit(form, id, update=False):
    if update is False:
        article = {
            'yb_id': id,
            'title': form.get('title'),
            'content': form.get('content')
        }
        insert_article(article)
    else:
        article = {
            'article_id': id,
            'title': form.get('title'),
            'content': form.get('content')
        }
        update_article(article)


def delete_user_article(article_id):
    delete_article(article_id)
