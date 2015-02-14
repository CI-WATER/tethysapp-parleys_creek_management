import time

from ckan.lib.base import BaseController
import ckan.plugins as p

from ..models import SessionMaker, ManagementScenario
from ..models import (LITTLE_DELL_VOLUME,
                      LITTLE_DELL_RELEASE,
                      LITTLE_DELL_SPILL,
                      MOUNTAIN_DELL_VOLUME,
                      MOUNTAIN_DELL_RELEASE,
                      MOUNTAIN_DELL_SPILL,
                      DELL_CREEK_INFLOW,
                      LAMBS_CREEK_INFLOW,
                      RELIABILITY)

class ResultsController(BaseController):
    '''
    Controller for input workflow form
    '''    
    
    def view(self):
        '''
        Default action for results controller
        '''
        t = p.toolkit
        c = t.c
        _ = t._
        
        session = SessionMaker()
        scenario = session.query(ManagementScenario.name,
                                 ManagementScenario.results_link,
                                 ManagementScenario.reliability).\
                           filter(ManagementScenario.id == c.id).\
                           one()
        
        # Access Plot data            
        datasource = ManagementScenario.get_results_dataset(c.id, c.plot_name)
            
        # Other data for template
        c.scenario_name = scenario.name
        c.results_link = scenario.results_link
        c.reliability = scenario.reliability
        
        # Pass names of plots to the template
        c.LITTLE_DELL_VOLUME = LITTLE_DELL_VOLUME
        c.LITTLE_DELL_RELEASE = LITTLE_DELL_RELEASE
        c.LITTLE_DELL_SPILL = LITTLE_DELL_SPILL
        c.MOUNTAIN_DELL_VOLUME = MOUNTAIN_DELL_VOLUME
        c.MOUNTAIN_DELL_RELEASE = MOUNTAIN_DELL_RELEASE
        c.MOUNTAIN_DELL_SPILL = MOUNTAIN_DELL_SPILL
        c.DELL_CREEK_INFLOW = DELL_CREEK_INFLOW
        c.LAMBS_CREEK_INFLOW = LAMBS_CREEK_INFLOW
        c.RELIABILITY = RELIABILITY
        
        # Plot vars
        plot_title = datasource['title']
        plot_subtitle = datasource['subtitle']
        y_axis_title = datasource['y_axis_title']
        y_axis_units = datasource['y_axis_units']
        series_data = datasource['series']
        
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
                    'maxZoom': 30 * 24 * 3600000, # 30 days in milliseconds
                },
                'yAxis': {
                    'title': {
                        'text': y_axis_title + ' (' + y_axis_units + ')'
                    }
                },
                'tooltip': {
                    'pointFormat': '{point.y} ' + y_axis_units
                 },
                'series': [{
                    'color': '#0066ff',
                    'marker' : {'enabled': False},
                    'data': series_data
                    }
                ]}
            
        c.timeseries = {'highcharts_object': highcharts_object,
                        'width': '100%',
                        'height': '500px'} 
        
        return t.render('ckanapp/parleys_creek_management/results/results_viewer.html')