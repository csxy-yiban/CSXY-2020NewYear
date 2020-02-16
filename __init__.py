from flask import (
    Flask, redirect, url_for, request
)
from flask import render_template
from pages.application.activity.new_year.article import *
from pages.application.activity.new_year.user import *
from pages.application.activity.new_year.feature import *
from pages.application.activity.new_year.form import *

app = Flask(__name__)
app.secret_key = "(0.0)"

code_request_url = "https://openapi.yiban.cn/oauth/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri
new_year_url = "/light-application/activity/new-year/"
new_year_src = "light application/activity/new year/"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/light-application')
def light_application():
    return render_template('light application/index.html')


@app.route('/wechat-mini-program')
def wechat_mini_program():
    return render_template('wechat-mini-program/index.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback/index.html')


@app.route('/login')
def login():
    code = request.args.get('code')
    access_info = get_access_token(code).json()
    info = user_info(access_info)
    if info is None:
        return render_template(new_year_src + "400.html", content=access_info['info'])
    if info['status'] == 'error':
        return render_template(new_year_src + "400.html", content=info['info'])
    update_user(access_info["access_token"])
    return redirect(url_for('new_year'))


def login_test():
    login_status = is_login()
    if login_status is False:
        return redirect(code_request_url)
    return None


@app.route('/logout')
def logout():
    status_code = remove_token(get_session()["access_token"])
    drop_session()
    if status_code != "error":
        return redirect(url_for("new_year"))
    else:
        return render_template(new_year_src + "400.html", content="注销错误？在微信公众号(城院易班学生工作站)反馈情况")


@app.route('/light-application/activity')
def activity():
    return render_template('light application/activity/index.html')


@app.route(new_year_url)
def new_year():
    return render_template(new_year_src + 'index.html', articles=get_all_articles(), user=get_session())


@app.route(new_year_url + '<int:yb_id>')
def new_year_user(yb_id):
    test = login_test()
    if test is not None:
        return test
    return render_template(new_year_src + "my-article.html", articles=user_articles(yb_id), user=get_session(),
                           can_delete=True)


@app.route(new_year_url + '<int:yb_id>/add-article', methods=['GET', 'POST'])
def new_year_add_article(yb_id):
    test = login_test()
    if test is not None:
        return test
    add_article = AddArticle()
    if request.method == 'POST':
        article_submit(request.form, yb_id)
        return redirect(url_for('new_year_user', yb_id=yb_id))
    return render_template(new_year_src + "add-article.html", user=get_session(), form=add_article, do="添加文章")


@app.route(new_year_url + 'article/<int:article_id>')
def new_year_article(article_id):
    test = login_test()
    if test is not None:
        return test
    comments = article_comments(article_id)
    if not comments:
        comments = 0
    return render_template(new_year_src + "article.html", article=get_article(article_id), comments=comments,
                           user=get_session(), form=AddComment())


@app.route(new_year_url + 'article/delete/<int:article_id>')
def new_year_article_delete(article_id):
    delete_user_article(article_id)
    delete_article_comment(article_id)
    delete_article_prise(article_id)
    return redirect(request.referrer)


@app.route(new_year_url + 'article/change/<int:article_id>', methods=['GET', 'POST'])
def new_year_article_change(article_id):
    if request.method == 'POST':
        article_submit(request.form, id=article_id, update=True)
        return redirect(url_for('new_year_user', yb_id=get_session()['yb_id']))
    return render_template(new_year_src + "add-article.html", user=get_session(), form=ChangeArticle(article_id),
                           do="修改文章", article=get_article(article_id))


@app.route(new_year_url + 'comment/delete/<int:comment_id>')
def new_year_comment_delete(comment_id):
    delete_user_comment(comment_id)
    return redirect(request.referrer)


@app.route(new_year_url + 'article/<int:article_id>/comment_add/<int:reply_id>', methods=['POST'])
def new_year_add_comment(article_id, reply_id):
    if reply_id == 0:
        reply_id = None
    comment_submit(form=request.form, article_id=article_id, yb_id=get_session()['yb_id'], reply_id=reply_id)
    return redirect(request.referrer)


@app.route(new_year_url + 'prise/', methods=['POST'])
def new_year_article_prise():
    return prise_request(request.form)
