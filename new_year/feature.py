from pages.application.activity.new_year.db import (
    get_comments, get_comment_by_id, delete_comment, insert_comment, insert_prise, delete_prise,
    get_prise_by_user_and_article, delete_comments, delete_prises, change_comment_replys
)
from pages.application.activity.new_year.user import get_user_info_from_database


def article_comments(article_id):
    comments_data = get_comments(article_id)
    comments = []
    for data in comments_data:
        if data[3] is None:
            reply_user = None
        else:
            reply_comment = get_comment_by_id(data[3])
            reply_user = get_user_info_from_database(reply_comment[2])['name']
        comments.append({
            'user': get_user_info_from_database(data[2]),
            'comment_id': data[0],
            'reply': reply_user,
            'content': data[4],
            'date': data[5]
        })
    return comments


def article_comment_amount(article_id):
    return len(get_comments(article_id))


def comment_submit(form, article_id, yb_id, reply_id):
    comment = {
        "article_id": article_id,
        "yb_id": yb_id,
        "reply_id": reply_id,
        "content": form.get('content')
    }
    insert_comment(comment)


def delete_user_comment(comment_id):
    delete_comment(comment_id)
    change_comment_replys(comment_id)


def article_is_prise(article_id, yb_id):
    return '1' if get_prise_by_user_and_article(article_id, yb_id) is not None else '0'


def article_prise_change(status, article_id, yb_id):
    if status == "insert":
        insert_prise(article_id, yb_id)
    else:
        delete_prise(article_id, yb_id)


def prise_request(form):
    status = form.get('status')
    article_id = form.get('article_id')
    yb_id = form.get('yb_id')
    if status == "get":
        return article_is_prise(article_id, yb_id)
    else:
        article_prise_change(status, article_id, yb_id)
        return "success"


def delete_article_comment(article_id):
    delete_comments(article_id)


def delete_article_prise(article_id):
    delete_prises(article_id)
