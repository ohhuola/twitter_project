import random


from pyecharts import Grid, Line, Pie, HeatMap,Map
from pyecharts.conf import PyEchartsConfig
from pyecharts.engine import EchartsEnvironment
from pyecharts.utils import write_utf8_html_file

from . import main
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import Twitter, Tweet
from app.main.forms import UserForm,SearchForm
from . import main

logger = get_logger(__name__)
cfg = get_config()

def common_manage(DynamicModel,view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)

#查询用户界面显示
def common_search(DynamicModel,TweetModel,form,view):
    tweet={}
    time=[]
    if form.validate_on_submit():
        try:
            DModel=DynamicModel()
            utils.form_to_model(form, DModel)
            dict = utils.obj_to_dict(DModel)
            name=dict['user_name']
            DModel = DynamicModel.get(name==DynamicModel.user_name)
            dict = utils.obj_to_dict(DModel)
            info, tags, exurls, mention_names = utils.dict_to_text(dict)

            TModel=TweetModel()
            query=TModel.select().where(TweetModel.tweet_user_name==name)
            for i in query:
                tweet[i.tweets]=i.time
                time.append(i.time)

            test=[12,43,65,76,8]
            return render_template('personInfo.html',tweet=tweet,time=time,freq=test, form=info,urls=exurls,tags=tags,friends=mention_names, current_user=current_user)
        except Exception as e:
            print (e)

            return render_template('errors/404.html')
    else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


def common_adduser(DynamicModel,form,view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)

# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    value = [95.1, 23.2, 43.3, 66.4, 88.5]
    attr = ["China", "Canada", "Brazil", "Russia", "United States"]
    map = Map("世界地图示例", width=1200, height=600)
    map.add(
        "",
        attr,
        value,
        maptype="world",
        is_visualmap=True,
        visual_text_color="#000",
    )
    return render_template('index.html',
                           myechart=map.render_embed(),
                           host=REMOTE_HOST,
                           script_list=map.get_js_dependencies(),
                           current_user=current_user)

#用户管理
@main.route('/manage',methods=['GET','POST'])
@login_required
def manage():
    return common_manage(Twitter, 'managelist.html')

#增加用户
@main.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    return common_adduser(Twitter,UserForm(),'Adduser.html')


#查詢用戶界面
@main.route('/searchpage',methods=['GET','POST'])
@login_required
def searchpage():
    return common_search(Twitter,Tweet,SearchForm(),'Searchuser.html')

#测试页面
@main.route('/test')
@login_required
def test():
    return render_template('test.html')
