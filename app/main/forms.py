from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,  SelectField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    user_name=StringField('用户名字',validators=[DataRequired(message='不能为空'),Length(0,200,message='长度不正确')])
    user_nick =StringField('用户昵称', validators=[DataRequired(message='不能为空'), Length(0, 200, message='长度不正确')])
    number_of_tweets=StringField('累计发推数量',validators=[Length(0,200,message='长度不正确')])
    recent_active_time=StringField('最近活跃时间',validators=[DataRequired(message='不能为空'),Length(0,200,message='长度不正确')])
    user_mentions_name = StringField('提及用户名称', validators=[Length(0, 255, message='长度不正确')])
    hastags = StringField('使用标签', validators=[Length(0, 200, message='长度不正确')])
    exurl = StringField('链接', validators=[Length(0, 10000, message='长度不正确')])
    submit = SubmitField('提交')
    # rencet_active_time使用StringField还是DateField有待商榷

class SearchForm(FlaskForm):
    user_name = StringField('用户名字', validators=[DataRequired(message='不能为空'), Length(0, 200, message='长度不正确')])
    user_nick = StringField('用户昵称', validators=[Length(0, 255, message='长度不正确')])
    number_of_tweets = StringField('累计发推数量', validators=[Length(0, 255, message='长度不正确')])
    recent_active_time = StringField('最近活跃时间', validators=[Length(0, 255, message='长度不正确')])
    user_mentions_name = StringField('提及用户名称', validators=[Length(0, 255, message='长度不正确')])
    hastags = StringField('使用标签', validators=[Length(0, 200, message='长度不正确')])
    exurl = StringField('链接', validators=[Length(0, 10000, message='长度不正确')])
    submit = SubmitField('Go')