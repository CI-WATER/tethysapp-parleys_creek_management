import os
from datetime import datetime
from time import time

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from xlrd import open_workbook, xldate_as_tuple
from itertools import izip

from ..model import ManagementScenario, SessionMaker
from ..model import (LITTLE_DELL_VOLUME,
                     LITTLE_DELL_RELEASE,
                     LITTLE_DELL_SPILL,
                     MOUNTAIN_DELL_VOLUME,
                     MOUNTAIN_DELL_RELEASE,
                     MOUNTAIN_DELL_SPILL,
                     DELL_CREEK_INFLOW,
                     LAMBS_CREEK_INFLOW,
                     RELIABILITY)

from ..lib.goldsim import runLittleDellGoldSim
from ..lib import get_package_name, CKAN_ENGINE


def jobs(request):
    """
    Start a new scenario in the scenario table
    """
    # Get user id
    user_id = request.user.id

    # Get a session
    session = SessionMaker()
    scenarios_list = session.query(ManagementScenario.id,
                                   ManagementScenario.name,
                                   ManagementScenario.description,
                                   ManagementScenario.last_updated,
                                   ManagementScenario.job_status,
                                   ManagementScenario.percentage,
                                   ManagementScenario.results_link). \
        filter(ManagementScenario.user_id == str(user_id)). \
        order_by(ManagementScenario.last_updated.desc()). \
        all()

    # Initialize paginator
    page_number = request.GET.get('page')
    paginator = Paginator(scenarios_list, 10)

    # Define pager format
    pager_format = '''
                   <ul class="pagination">
                     <li><a href="#">1</a></li>
                     <li><a href="#">1</a></li>
                     <li><a href="#">1</a></li>
                   </ul>
                   '''
    try:
        # Return the requested page
        scenarios = paginator.page(page_number)

    except PageNotAnInteger:
        # Deliver first page if page is not an integer
        scenarios = paginator.page(1)

    except EmptyPage:
        # Deliver last page if page number is out of range
        scenarios = paginator.page(len(scenarios_list))

    # Template context
    context = {'scenarios': scenarios,
               'paginator': paginator,
               'statuses': ('pending', 'success', 'error'),
               'nav': 'scenarios'}

    return render(request, 'parleys_creek_management/jobs/jobs.html', context)


def delete(request, scenario_id):
    """
    Delete the scenario
    """
    # Retrieve the scenario
    session = SessionMaker()
    scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Delete the current scenario
    session.delete(scenario)
    session.commit()

    return redirect('parleys_creek_management:jobs')


def status(request, scenario_id):
    """
    Return job status information for a job
    """
    # Get user id
    user_id = str(request.user.id)

    # Get a session
    session = SessionMaker()
    scenario = session.query(ManagementScenario).get(scenario_id)

    # Defaults
    job_status = None
    percentage = None
    link = None

    if scenario and scenario.user_id == user_id:
        job_status = scenario.job_status
        percentage = scenario.percentage
        link = reverse('parleys_creek_management:results_view',
                       kwargs={'scenario_id': scenario_id, 'plot_name': 'little-dell-volume'})

    # Form response
    if percentage >= 100:
        json_response = {'status': job_status, 'percentage': percentage, 'link': link}
    else:
        json_response = {'status': job_status, 'percentage': percentage, 'link': None}

    return JsonResponse(json_response)


def run(request, scenario_id):
    """
    Run the model action
    """
    # Get user id
    user_id = str(request.user.id)

    # Get a session
    session = SessionMaker()
    scenario = session.query(ManagementScenario). \
        filter(ManagementScenario.user_id == user_id). \
        filter(ManagementScenario.id == scenario_id). \
        one()

    scenario.job_status = 'processing'
    scenario.percentage = 0
    session.commit()

    # Get arguments for the web service
    arguments = scenario.get_web_service_inputs()

    # Get Path to Workspace and unique file name
    workspace_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'workspace')
    unique_file_name = request.user.username + datetime.now().strftime('%Y%d%m%H%M%S') + '.xls'
    out_path = os.path.join(workspace_dir, unique_file_name)

    # Update status of scenario in the database to processing
    scenario.percentage = 25
    session.commit()

    # Set timeout to be 10 minutes
    timeout = time() + 3 * 60  # seconds
    frequency = 3  # seconds

    # If timeout occurs, will be marked as error
    job_status = 'error'
    error_message = ''

    # Start execution
    execution = runLittleDellGoldSim(arguments, out_path)

    # Check status until time-out happens
    while not execution.isComplete():
        if time() >= timeout:
            # kill request
            break

        execution.checkStatus(sleepSecs=frequency)

    if execution.isSucceded():
        # Update status in db
        scenario.job_status = 'downloading results'
        scenario.percentage = 50
        session.commit()

        # Get results
        execution.getOutput(out_path)
        job_status = 'success'

        # Get package name from app.ini
        package_name = get_package_name()
        result = {'success': False}

        # Push file to ckan dataset
        try:
            # Push file to ckan dataset
            resource_name = scenario.name
            description = '{0} \<Created by {1} on {2}\>'.format(scenario.description, request.user.username,
                                                                 datetime.now().strftime('%B, %d %Y @ %H:%M'))
            result = CKAN_ENGINE.create_resource(dataset_id=package_name, file=out_path, name=resource_name,
                                                 format='xls', model='PCMT-GOLDSIM', description=description)
        except Exception as e:
            error_message = 'PCMT RUN WARNING: {0}'.format(e.message)
            job_status = 'error'
            print(error_message)

        # Get link of the resource
        if result['success']:
            results_link = result['result']['url']
        else:
            error_message = 'PCMT RUN WARNING: Job execution failed.'
            results_link = None
            job_status = 'error'
            print(error_message)

        # Parse results into python data structures and cache in database for visualization
        scenario.job_status = 'processing results'
        scenario.percentage = 75
        session.commit()

        try:
            parsed_results = parse_results(out_path)
            scenario.set_results(parsed_results)
        except Exception as e:
            error_message = 'PCMT RUN WARNING: {0}'.format(e.message)
            job_status = 'error'
            print(error_message)

        # Delete temp file in workspace
        try:
            os.remove(out_path)
        except Exception as e:
            error_message = 'PCMT RUN WARNING: {0}'.format(e.message)
            print(error_message)

        # Update the scenario job status
        scenario.results_link = results_link

    # Update status in db
    scenario.job_status = job_status
    scenario.percentage = 100
    session.commit()

    results_link = scenario.results_link

    # Assemble response object
    if error_message != '':
        json_response = {'status': job_status, 'link': results_link}
    else:
        json_response = {'status': job_status, 'link': results_link, 'message': error_message}

    session.close()

    return JsonResponse(json_response)


def parse_results(filename):
    """
    This method is used to parse the results into Python data structures.
    """
    results = dict()

    # Get a handle on the workbook
    workbook = open_workbook(filename)

    # Get handles on the sheets
    little_dell = workbook.sheet_by_index(0)
    mountain_dell = workbook.sheet_by_index(1)
    inflows = workbook.sheet_by_index(2)
    reliability = workbook.sheet_by_index(3)

    for sheet_index in range(workbook.nsheets):
        sheet = workbook.sheet_by_index(sheet_index)
        sheet_name = sheet.name

        if sheet_name == 'Little Dell':
            little_dell = sheet
        elif sheet_name == 'Mountain Dell':
            mountain_dell = sheet
        elif sheet_name == 'Lambs and Dell Creeks':
            inflows = sheet
        elif sheet_name == 'Reliability':
            reliability = sheet

    ##
    # Little Dell
    ##

    # Parse Sheet and hack of headers (top three rows)
    ld_time = little_dell.col_values(0)[3:]
    ld_volume = little_dell.col_values(1)[3:]
    ld_release = little_dell.col_values(2)[3:]
    ld_spill = little_dell.col_values(3)[3:]

    # Convert decimal date to datetime
    ld_datetime = []

    for dec_time in ld_time:
        time_tuple = xldate_as_tuple(dec_time, workbook.datemode)
        ld_datetime.append(datetime(*time_tuple))

    # Stitch together
    ld_volume_series = [list(i) for i in izip(ld_datetime, ld_volume)]
    ld_release_series = [list(i) for i in izip(ld_datetime, ld_release)]
    ld_spill_series = [list(i) for i in izip(ld_datetime, ld_spill)]

    # Create series dictionaries
    ld_volume_dict = {'title': 'Little Dell Volume',
                      'subtitle': '',
                      'y_axis_title': 'Volume',
                      'y_axis_units': 'kaf',
                      'series': ld_volume_series}

    results[LITTLE_DELL_VOLUME] = ld_volume_dict

    ld_release_dict = {'title': 'Little Dell Release',
                       'subtitle': '',
                       'y_axis_title': 'Flowrate',
                       'y_axis_units': 'af/d',
                       'series': ld_release_series}

    results[LITTLE_DELL_RELEASE] = ld_release_dict

    ld_spill_dict = {'title': 'Little Dell Spills',
                     'subtitle': '',
                     'y_axis_title': 'Flowrate',
                     'y_axis_units': 'af/d',
                     'series': ld_spill_series}

    results[LITTLE_DELL_SPILL] = ld_spill_dict

    ##
    # Mountain Dell
    ##

    # Parse Sheet and hack of headers (top three rows)
    md_time = mountain_dell.col_values(0)[3:]
    md_volume = mountain_dell.col_values(1)[3:]
    md_release = mountain_dell.col_values(2)[3:]
    md_spill = mountain_dell.col_values(3)[3:]

    # Convert decimal date to datetime
    md_datetime = []

    for dec_time in md_time:
        time_tuple = xldate_as_tuple(dec_time, workbook.datemode)
        md_datetime.append(datetime(*time_tuple))

    # Stitch together
    md_volume_series = [list(i) for i in izip(md_datetime, md_volume)]
    md_release_series = [list(i) for i in izip(md_datetime, md_release)]
    md_spill_series = [list(i) for i in izip(md_datetime, md_spill)]

    # Create series dictionaries
    md_volume_dict = {'title': 'Mountain Dell Volume',
                      'subtitle': '',
                      'y_axis_title': 'Volume',
                      'y_axis_units': 'kaf',
                      'series': md_volume_series}

    results[MOUNTAIN_DELL_VOLUME] = md_volume_dict

    md_release_dict = {'title': 'Mountain Dell Release',
                       'subtitle': '',
                       'y_axis_title': 'Flowrate',
                       'y_axis_units': 'af/d',
                       'series': md_release_series}

    results[MOUNTAIN_DELL_RELEASE] = md_release_dict

    md_spill_dict = {'title': 'Mountain Dell Spills',
                     'subtitle': '',
                     'y_axis_title': 'Flowrate',
                     'y_axis_units': 'af/d',
                     'series': md_spill_series}

    results[MOUNTAIN_DELL_SPILL] = md_spill_dict

    ##
    # Inflows
    ##

    # Parse Sheet and hack of headers (top three rows)
    inflow_time = inflows.col_values(0)[3:]
    inflow_dell_creek = inflows.col_values(1)[3:]
    inflow_lamb_creek = inflows.col_values(2)[3:]

    # Convert decimal date to datetime
    inflow_datetime = []

    for dec_time in inflow_time:
        time_tuple = xldate_as_tuple(dec_time, workbook.datemode)
        inflow_datetime.append(datetime(*time_tuple))

    # Stitch together
    dell_creek_series = [list(i) for i in izip(inflow_datetime, inflow_dell_creek)]
    lamb_creek_series = [list(i) for i in izip(inflow_datetime, inflow_lamb_creek)]

    # Create series dictionaries
    dell_creek_dict = {'title': 'Dell Creek Inflow',
                       'subtitle': '',
                       'y_axis_title': 'Flowrate',
                       'y_axis_units': 'cfs',
                       'series': dell_creek_series}

    results[DELL_CREEK_INFLOW] = dell_creek_dict

    lamb_creek_dict = {'title': 'Lambs Creek Inflow',
                       'subtitle': '',
                       'y_axis_title': 'Flowrate',
                       'y_axis_units': 'cfs',
                       'series': lamb_creek_series}

    results[LAMBS_CREEK_INFLOW] = lamb_creek_dict

    ##
    # Reliability
    ##

    results[RELIABILITY] = reliability.cell_value(3, 6)
    print results[RELIABILITY]

    return results