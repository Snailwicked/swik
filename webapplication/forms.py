from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField
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
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')
