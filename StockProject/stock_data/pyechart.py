# ...
from django_echarts.starter.sites import DJESite
from django_echarts.entities import Copyright
from pyecharts import options as opts
from pyecharts.charts import Bar

site_obj = DJESite(site_title='福建统计')

site_obj.add_widgets(copyright_=Copyright(start_year=2022, powered_by='Zinc'))

chart_description = '截止2020年底，福建省土地面积1240.29万公顷，占我国国土总面积1.3%。全省森林面积811.58万公顷，森林覆盖率为66.8%，连续42年位居全国首位。'

@site_obj.register_chart(title='森林覆盖率', description = chart_description, catalog='基本信息')
def fujian_forest_coverage():
    bar = Bar().add_xaxis(
        ['福州', '厦门', '莆田', '三明', '漳州', '泉州', '南平', '龙岩', '宁德']
    ).add_yaxis(
        '森林覆盖率', [54.7, 45, 58.1, 76.8, 63.4, 61, 75.3, 78, 75]
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="福建省各地市森林覆盖率", subtitle="单位：%"),
        visualmap_opts=opts.VisualMapOpts(is_show=True, max_=100, min_=0)).set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(y=66.8, name="全省"),
            ]
        )
    )
    return bar
