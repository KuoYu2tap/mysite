# Create your views here.

from itertools import groupby

from django.db.models import Sum
from django.shortcuts import HttpResponse
from django.template import loader
from pyecharts import Pie, Timeline

from account.models import Account


def draw_pie_all_cost():
    _all = Account.objects.values("spent_date", "reason").annotate(Sum("cost")).order_by("spent_date")
    d = dict(
        (i, list(j)) for i, j in
        groupby(_all, key=lambda x: (x['spent_date'].year, x['spent_date'].month))
    )
    timeline = Timeline(is_auto_play=False, timeline_bottom=0, width=800, height=500)

    # TODO:最大问题在于，如果有未显示的字段，会导致饼图颜色分类的不一致
    # TODO: 开始展示折线图，然后点击折线图可以跳转
    CHOICE = dict(Account.TAGS_CHOICE)  # 名字
    i = 0
    for k, v in d.items():
        dict_cost = {CHOICE[_['reason']]: _['cost__sum'] for _ in v}
        cost_pie = Pie("{}年{}月".format(*k), "总开销{}元".format(sum(dict_cost.values()), width=800, height=100))
        cost_pie.add("{}-{}".format(*k), dict_cost.keys(), dict_cost.values(),
                     radius=[30, 75], is_label_show=True)
        timeline.add(cost_pie, "{}-{}".format(*k))
        i += 1
        if i > 5:
            break
    return timeline



def index(request):
    template = loader.get_template('account/detail.html')
    timeline = draw_pie_all_cost()
    context = dict(
        myechart=timeline.render_embed(),
        host='/static/echarts/js',
        script_list=timeline.get_js_dependencies(),
    )
    return HttpResponse(template.render(context, request))
