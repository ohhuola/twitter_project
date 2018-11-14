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
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main

logger = get_logger(__name__)
cfg = get_config()

# 通用列表查询
def common_list(DynamicModel, view):
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


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    print(request.args)
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


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')

def draft():
    heatmap = HeatMap(width=600, height=300)
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    y = ['Mon', 'Tues', 'Wen', 'Tues', 'Fri', 'Sat', 'Sun']
    data = [[i, j, random.randint(0, 50)] for i in range(12) for j in range(7)]
    heatmap.add(
        "heatmap",
        x,
        y,
        data,
        is_visualmap=True,
        visual_text_color='blue',
        visual_orient='horizontal',
        visvual_pos='right',
        visual_bottom='5%'
    )
    config = PyEchartsConfig(echarts_template_dir='app/templates', jshost='app/static/js')
    # 创建echart的运行环境,主要是为了确认文件存放取出的文件夹,和js依赖文件引入的来源
    env = EchartsEnvironment(pyecharts_config=config)
    tpl = env.get_template('demo.html')  # 提取模板文件
    html = tpl.render(heatmap=heatmap)  # 渲染
    write_utf8_html_file('app/templates/index2.html', html)






