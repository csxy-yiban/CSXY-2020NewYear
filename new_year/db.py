import pymysql


def connect():
    host = "localhost"
    user = "root"
    password = "xxxxxx"
    database = "new_year_application"
    return pymysql.connect(host, user, password, database)


def executor(sql, values):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
    finally:
        connection.commit()
        connection.close()


def fetchone(sql, value):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, value)
            fetch_result = cursor.fetchone()
    finally:
        connection.close()
    return fetch_result


def fetchall(sql, value):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, value)
            fetch_result = cursor.fetchall()
    finally:
        connection.close()
    return fetch_result


def get_articles():
    sql = "select * from articles;"
    return fetchall(sql, None)


def get_user_info_by_id(yb_id):
    sql = "select * from users where yb_id=%s;"
    return fetchone(sql, yb_id)


def delete_user(yb_id):
    sql = "delete from users where yb_id=%s;"
    executor(sql, yb_id)


def get_article_by_id(article_id):
    sql = 'select * from articles where article_id=%s;'
    return fetchone(sql, article_id)


def get_articles_by_user(yb_id):
    sql = 'select * from articles where yb_id=%s;'
    return fetchall(sql, yb_id)


def get_prises(article_id):
    sql = "select * from prises where article_id=%s;"
    return fetchall(sql, article_id)


def get_comments(article_id):
    sql = "select * from comments where article_id=%s;"
    return fetchall(sql, article_id)


def get_comment_by_id(comment_id):
    sql = "select * from comments where comment_id=%s;"
    return fetchone(sql, comment_id)


def insert_user(info):
    sql = "insert into users (name,yb_id,head) value (%s,%s,%s);"
    values = (info['name'], info['yb_id'], info['head'])
    executor(sql, values)


def insert_article(article):
    sql = "insert into articles (article_id,yb_id,title,content,datetime) values (null,%s,%s,%s,now());"
    values = (article['yb_id'], article['title'], article['content'])
    executor(sql, values)


def update_article(article):
    sql = "update articles set title=%s,content=%s where article_id=%s;"
    values = (article['title'], article['content'], article['article_id'])
    executor(sql, values)


def delete_article(article_id):
    sql = "delete from articles where article_id=%s;"
    executor(sql, article_id)


def insert_comment(comment):
    sql = "insert into comments (comment_id,article_id,yb_id,reply_id,content,datetime" \
          ") values (" \
          "null,%s,%s,%s,%s,now());"
    values = (comment['article_id'], comment['yb_id'], comment['reply_id'], comment['content'])
    executor(sql, values)


def delete_comment(comment_id):
    sql = "delete from comments where comment_id=%s;"
    executor(sql, comment_id)


def insert_prise(article_id, yb_id):
    sql = "insert into prises (article_id,yb_id) values (%s,%s);"
    executor(sql, (article_id, yb_id))


def delete_prise(article_id, yb_id):
    sql = "delete from prises where article_id=%s and yb_id=%s;"
    executor(sql, (article_id, yb_id))


def get_prise_by_user_and_article(article_id, yb_id):
    sql = "select * from prises where article_id=%s and yb_id=%s"
    return fetchone(sql, (article_id, yb_id))


def delete_comments(article_id):
    sql = "delete from comments where article_id=%s;"
    executor(sql, article_id)


def change_comment_replys(comments_id):
    sql = "update comments set reply_id=null where reply_id=%s;"
    executor(sql, comments_id)


def delete_prises(article_id):
    sql = "delete from prises where article_id=%s;"
    executor(sql, article_id)
