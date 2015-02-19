from django.shortcuts import render

from ..model import SessionMaker, ManagementScenario
from ..model import (LITTLE_DELL_VOLUME,
                     LITTLE_DELL_RELEASE,
                     LITTLE_DELL_SPILL,
                     MOUNTAIN_DELL_VOLUME,
                     MOUNTAIN_DELL_RELEASE,
                     MOUNTAIN_DELL_SPILL,
                     DELL_CREEK_INFLOW,
                     LAMBS_CREEK_INFLOW,
                     RELIABILITY)


def view(request, scenario_id, plot_name):
    """
    Default action for results controller
    """
    session = SessionMaker()
    scenario = session.query(ManagementScenario.name,
                             ManagementScenario.results_link,
                             ManagementScenario.reliability). \
        filter(ManagementScenario.id == scenario_id). \
        one()

    # Access Plot data
    data_source = ManagementScenario.get_results_dataset(scenario_id, plot_name)

    # Other data for template
    scenario_name = scenario.name
    results_link = scenario.results_link
    reliability = scenario.reliability

    # Plot vars
    plot_title = data_source['title']
    plot_subtitle = data_source['subtitle']
    y_axis_title = data_source['y_axis_title']
    y_axis_units = data_source['y_axis_units']
    series_data = data_source['series']

    # Setup plot
    highcharts_object = {
        'chart': {
            'type': 'line',
            'zoomType': 'x'
        },
        'title': {
            'text': plot_title
        },
        'subtitle': {
            'text': plot_subtitle
        },
        'legend': {
            'enabled': False,
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle',
            'borderWidth': 0
        },
        'xAxis': {
            'title': {
                'enabled': False
            },
            'type': 'datetime',
            'maxZoom': 30 * 24 * 3600000,  # 30 days in milliseconds
        },
        'yAxis': {
            'title': {
                'text': y_axis_title + ' (' + y_axis_units + ')'
            }
        },
        'tooltip': {
            'pointFormat': '{point.y} ' + y_axis_units
        },
        'series': [{'color': '#0066ff',
                    'marker': {'enabled': False},
                    'data': series_data}
        ]
    }

    timeseries = {'highcharts_object': highcharts_object,
                  'width': '100%',
                  'height': '500px'}

    # Template context
    context = {'scenario_name': scenario_name,
               'results_link': results_link,
               'reliability': reliability,
               'LITTLE_DELL_VOLUME': LITTLE_DELL_VOLUME,
               'LITTLE_DELL_RELEASE': LITTLE_DELL_RELEASE,
               'LITTLE_DELL_SPILL': LITTLE_DELL_SPILL,
               'MOUNTAIN_DELL_VOLUME': MOUNTAIN_DELL_VOLUME,
               'MOUNTAIN_DELL_RELEASE': MOUNTAIN_DELL_RELEASE,
               'MOUNTAIN_DELL_SPILL': MOUNTAIN_DELL_SPILL,
               'DELL_CREEK_INFLOW': DELL_CREEK_INFLOW,
               'LAMBS_CREEK_INFLOW': LAMBS_CREEK_INFLOW,
               'RELIABILITY': RELIABILITY,
               'timeseries': timeseries}

    return render(request, 'parleys_creek_management/results/results_viewer.html', context)