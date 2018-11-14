from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class CfgNotifyForm(FlaskForm):
    check_order = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_name = StringField('通知人姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_number = StringField('通知号码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')

class UserForm(FlaskForm):
    tweet_user_name=StringField('用户名字',validators=[DataRequired(message='不能为空'),Length(0,200,message='长度不正确')])
    tweet_user_nick =StringField('用户昵称', validators=[DataRequired(message='不能为空'), Length(0, 200, message='长度不正确')])
    number_of_tweets=StringField('累计发推数量',validators=[DataRequired(message='不能为空'),Length(0,200,message='长度不正确')])
    recent_active_time=StringField('最近活跃时间',validators=[DataRequired(message='不能为空'),Length(0,200,message='长度不正确')])
    submit = SubmitField('提交')
    # rencet_active_time使用StringField还是DateField有待商榷