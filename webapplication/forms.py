from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class TodoListForm(FlaskForm):
    url = StringField('网址', validators=[DataRequired(), Length(1, 64)])
    web_name = StringField('名称', validators=[DataRequired(), Length(1, 32)])
    agent = StringField('代理', validators=[DataRequired(), Length(1, 32)])
    status = StringField('状态', validators=[DataRequired(), Length(1, 32)])
    # status = RadioField('是否完成', validators=[DataRequired()],  choices=[("1", '是'),("0",'否')])
    sort = StringField('类型', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('账户', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')


# class SearchForm(FlaskForm):
#     start_time = DateTimeField('开始时间', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired(), Length(1, 20)])
#     end_time = DateTimeField('结束时间', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired(), Length(1, 20)])
#     search_name = StringField('请输入网站名称', validators=[DataRequired(), Length(1, 64)])
#     submit = SubmitField('搜索')


class WaitedTaskForm(FlaskForm):
    # waited_crawl = SubmitField('未启动网站')
    # crawl_deepth = SelectMultipleField('采集深度', choices=[('one', '1'), ('two', '2'), ('three', '3')]) 不用复选框
    limit = StringField('采集深度', validators=[DataRequired(), Length(1, 2)])
    submit = SubmitField('提交')
