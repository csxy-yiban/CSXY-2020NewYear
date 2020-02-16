from wtforms import Form, TextAreaField, validators, StringField, SubmitField
from pages.application.activity.new_year.article import get_article


class AddArticle(Form):
    title_feature = {
        'placeholder': '标题',
        'class': 'title-input'
    }
    content_feature = {
        'placeholder': '文章内容',
        'class': 'content-input'
    }
    title_validators = [
        validators.DataRequired(),
        validators.length(1, 20),
        validators.input_required
    ]
    content_validators = [
        validators.DataRequired(),
        validators.length(10, 5000),
        validators.input_required
    ]
    title = StringField(validators=title_validators, render_kw=title_feature)
    content = TextAreaField(validators=content_validators, render_kw=content_feature)
    submit = SubmitField("提交")


class AddComment(Form):
    content_validator = [
        validators.DataRequired(),
        validators.input_required,
        validators.length(0, 1000)
    ]
    content_feature = {
        "row": 5,
        'placeholder': "输入评论内容",
        "class": "comment-input"
    }
    content = TextAreaField(validators=content_validator, render_kw=content_feature)
    submit = SubmitField("发表")


class ChangeArticle(AddArticle):

    def __init__(self, article_id, **kwargs):
        super().__init__(**kwargs)
