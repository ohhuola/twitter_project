#encoding=utf-8

# @Time:2018/10/16 22:41
# @Author:wyx
# @File:echart.py

import random

from pyecharts import Grid, Line, Pie, HeatMap,Map
from flask import Flask, render_template

from . import main
REMOTE_HOST = "https://pyecharts.github.io/assets/js"


@main.route("/pyecharts")
def hello():


    attr1 = ["周一", "周二", "周三", "周四", "周五", "周六"]
    v2 = [55, 60, 16, 20, 15, 80]
    line = Line()
    #line.add("商家A", attr1, v1, mark_point=["average"])
    line.add("商家B",
             attr1,
             v2,
             mark_line=["max", "average"],
             legend_pos="20%",
             )

    v1 = [5, 20, 36, 10, 10, 100]
    attr2 = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    pie = Pie()
    pie.add(
        "",
        attr2,
        v1,
        radius=[40, 75],
        center=[65, 50],
        legend_orient="vertical",
        legend_pos="80%",
    )
    grid = Grid(width=1200)
    grid.add(line, grid_right="55%")
    grid.add(pie,grid_left="60%")

    return render_template(
        "pyecharts.html",
        myechart=grid.render_embed(),
        host=REMOTE_HOST,
        script_list=grid.get_js_dependencies(),

    )

