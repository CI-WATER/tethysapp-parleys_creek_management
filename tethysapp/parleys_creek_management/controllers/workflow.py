from datetime import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from ..model import SessionMaker, ManagementScenario
from ..lib import is_number, is_valid_name, is_valid_description


sc_number_key = {'0': 'Custom',
                 '1': 'Historical',
                 '2': 'Warm Wet',
                 '3': 'Warm Dry',
                 '4': 'Middle',
                 '5': 'Hot Wet',
                 '6': 'Hot Dry'}


def new(request):
    """
    Start a new scenario
    """
    # Create New Scenario
    new_scenario = ManagementScenario('Default', request.user.id)

    # Commit New Scenario
    session = SessionMaker()
    session.add(new_scenario)
    session.commit()

    # Get id
    scenario_id = new_scenario.id
    session.close()

    return redirect('parleys_creek_management:workflow_scenario', scenario_id=scenario_id)


def scenario(request, scenario_id):
    """
    Controller for the Scenario Selection form
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Handle form
    scenario_form_data = a_scenario.scenario

    sc_number = scenario_form_data['sc_number']

    scenario_name = a_scenario.name
    scenario_description = a_scenario.description

    # Error messages
    name_error = ''
    description_error = ''

    if 'nav_submit' in request.POST:
        # Validate form
        errors = False

        # Stash form values
        scenario_name = request.POST['scenario_name']
        scenario_description = request.POST['scenario_description']
        sc_number = request.POST['sc_number']

        # Validate alphanumeric
        if not is_valid_name(scenario_name):
            errors = True
            name_error = 'Invalid characters used'

        if not is_valid_description(scenario_description):
            errors = True
            description_error = 'Invalid characters used'

        # Update db if valid
        if not errors:
            a_scenario.name = scenario_name
            a_scenario.description = scenario_description
            a_scenario.scenario = dict(scenario_form_data.items() + dictize_params(request.POST).items())
            a_scenario.last_updated = datetime.now()
            session.commit()
            session.close()

            # Action of redirect given by value of submit button chosen
            action = request.POST['nav_submit']

            return redirect_to_action(action, scenario_id)

    # Configure form inputs
    name_input = {'display_text': 'Name',
                  'name': 'scenario_name',
                  'placeholder': 'e.g.: Run 1',
                  'initial': scenario_name,
                  'error': name_error
    }

    # Select Input
    select_input = {'display_text': 'Climate Scenario',
                    'name': 'sc_number',
                    'multiple': False,
                    'options': [(sc_number_key['1'], '1'),
                                (sc_number_key['2'], '2'),
                                (sc_number_key['3'], '3'),
                                (sc_number_key['4'], '4'),
                                (sc_number_key['5'], '5'),
                                (sc_number_key['6'], '6')],
                    'initial': [sc_number_key[sc_number]]
    }

    # Nav form action buttons
    cancel_btn = {'buttons': [{'display_text': 'Cancel',
                               'href': reverse('parleys_creek_management:workflow_cancel',
                                               kwargs={'scenario_id': scenario_id})}]
    }

    next_btn = {'buttons': [{'display_text': 'Next',
                             'name': 'nav_submit',
                             'style': 'success',
                             'attributes': 'value=general form=input-form',
                             'submit': True}]
    }

    context = {'scenario_name': scenario_name,
               'scenario_description': scenario_description,
               'description_error': description_error,
               'name_input': name_input,
               'select_input': select_input,
               'cancel_btn': cancel_btn,
               'next_btn': next_btn,
               'stage': 'scenario'
    }

    return render(request, 'parleys_creek_management/workflow/scenario.html', context)


def general(request, scenario_id):
    """
    Controller for the General Characteristics form
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Handle form
    general_form_data = a_scenario.general

    # Initialize the errors object
    error_messages = {'capacity_mt': '',
                      'init_mt': '',
                      'deadpool_mt': '',
                      'capacity_lit': '',
                      'init_lit': '',
                      'deadpool_lit': ''}

    if 'nav_submit' in request.POST:
        # Update with form data
        # Note: When two dictionaries are added together, the duplicate
        # keys are overwritten by the last dictionary
        general_form_data = dict(general_form_data.items() +
                                 dictize_params(request.POST).items())

        # Validate form parameters
        errors = False

        # Check that all are numbers and positive
        for key in error_messages:
            if not is_number(general_form_data[key]):
                errors = True
                error_messages[key] = 'Must be a number'

            elif int(general_form_data[key]) < 0:
                errors = True
                error_messages[key] = 'Must be a positive number'

        # Check that assumptions are met
        if not errors:
            # Initial volume must be less than capacity
            if int(general_form_data['capacity_mt']) < int(general_form_data['init_mt']):
                errors = True
                error_messages['init_mt'] = 'Initial volume must be less than capacity'

            if int(general_form_data['capacity_lit']) < int(general_form_data['init_lit']):
                errors = True
                error_messages['init_lit'] = 'Initial volume must be less than capacity'

            # Initial volume must be greater than dead pool
            if int(general_form_data['init_mt']) < int(general_form_data['deadpool_mt']):
                errors = True
                error_messages['deadpool_mt'] = 'Deadpool must be less than initial volume'

            if int(general_form_data['init_lit']) < int(general_form_data['deadpool_lit']):
                errors = True
                error_messages['deadpool_lit'] = 'Deadpool must be less than initial volume'

            # Dead pool must be less than capacity
            if int(general_form_data['capacity_mt']) < int(general_form_data['deadpool_mt']):
                errors = True
                error_messages['capacity_mt'] = 'Capacity must be greater than the deadpool'

            if int(general_form_data['capacity_lit']) < int(general_form_data['deadpool_lit']):
                errors = True
                error_messages['capacity_lit'] = 'Capacity must be greater than the deadpool'

        if not errors:
            # Update the database
            a_scenario.general = general_form_data
            a_scenario.last_updated = datetime.now()
            session.commit()

            # Action of redirect given by value of submit button chosen
            action = request.POST['nav_submit']

            return redirect_to_action(action=action, scenario_id=scenario_id)

    # Configure form inputs
    capacity_mt_input = {'display_text': 'Capacity',
                         'name': 'capacity_mt',
                         'placeholder': 'e.g.: 3200',
                         'initial': general_form_data['capacity_mt'],
                         'append': 'ac-ft',
                         'error': error_messages['capacity_mt']}

    init_mt_input = {'display_text': 'Initial Volume',
                     'name': 'init_mt',
                     'placeholder': 'e.g.: 800',
                     'initial': general_form_data['init_mt'],
                     'append': 'ac-ft',
                     'error': error_messages['init_mt']}

    deadpool_mt_input = {'display_text': 'Dead Pool',
                         'name': 'deadpool_mt',
                         'placeholder': 'e.g.: 2000',
                         'initial': general_form_data['deadpool_mt'],
                         'append': 'ac-ft',
                         'error': error_messages['deadpool_mt']}

    capacity_ld_input = {'display_text': 'Capacity',
                         'name': 'capacity_lit',
                         'placeholder': 'e.g.: 20000',
                         'initial': general_form_data['capacity_lit'],
                         'append': 'ac-ft',
                         'error': error_messages['capacity_lit']}

    init_ld_input = {'display_text': 'Initial Volume',
                     'name': 'init_lit',
                     'placeholder': 'e.g.: 5700',
                     'initial': general_form_data['init_lit'],
                     'append': 'ac-ft',
                     'error': error_messages['init_lit']}

    deadpool_ld_input = {'display_text': 'Dead Pool',
                         'name': 'deadpool_lit',
                         'placeholder': 'e.g.: 0',
                         'initial': general_form_data['deadpool_lit'],
                         'append': 'ac-ft',
                         'error': error_messages['deadpool_lit']}

    # Get scenario number
    sc_number = a_scenario.scenario['sc_number']

    # Skip inflow step if scenario is any other type beside historical
    if sc_number == '1':
        next_btn = {'buttons': [{'display_text': 'Next',
                                 'name': 'nav_submit',
                                 'style': 'success',
                                 'attributes': 'value=inflow form=input-form',
                                 'submit': True}]
        }

    else:
        next_btn = {'buttons': [{'display_text': 'Next',
                                 'name': 'nav_submit',
                                 'style': 'success',
                                 'attributes': 'value=demand form=input-form',
                                 'submit': True}]
        }

    # Other form action buttons
    cancel_btn = {'buttons': [{'display_text': 'Cancel',
                               'href': reverse('parleys_creek_management:workflow_cancel',
                                               kwargs={'scenario_id': scenario_id})}]
    }

    back_btn = {'buttons': [{'display_text': 'Back',
                             'name': 'nav_submit',
                             'attributes': 'value=scenario form=input-form',
                             'submit': True}]
    }

    # Context
    context = {
        'general_form_data': general_form_data,
        'cancel_btn': cancel_btn,
        'back_btn': back_btn,
        'capacity_mt_input': capacity_mt_input,
        'init_mt_input': init_mt_input,
        'deadpool_mt_input': deadpool_mt_input,
        'capacity_ld_input': capacity_ld_input,
        'init_ld_input': init_ld_input,
        'deadpool_ld_input': deadpool_ld_input,
        'next_btn': next_btn,
        'stage': 'general',
    }

    return render(request, 'parleys_creek_management/workflow/general.html', context)


def inflow(request, scenario_id):
    """
    Controller for the Monthly Inflow Rate form
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Handle form
    inflow_form_data = a_scenario.inflow

    if 'nav_submit' in request.POST:
        a_scenario.inflow = dict(inflow_form_data.items() + dictize_params(request.POST).items())
        a_scenario.last_updated = datetime.now()
        session.commit()
        session.close()

        # Action of redirect given by value of submit button chosen
        action = request.POST['nav_submit']

        return redirect_to_action(action=action, scenario_id=scenario_id)

    # Nav form action buttons
    cancel_btn = {'buttons': [{'display_text': 'Cancel',
                               'href': reverse('parleys_creek_management:workflow_cancel',
                                               kwargs={'scenario_id': scenario_id})}]
    }

    back_btn = {'buttons': [{'display_text': 'Back',
                             'name': 'nav_submit',
                             'attributes': 'value=general form=input-form',
                             'submit': True}]
    }

    next_btn = {'buttons': [{'display_text': 'Next',
                             'name': 'nav_submit',
                             'style': 'success',
                             'attributes': 'value=demand form=input-form',
                             'submit': True}]
    }

    # Form sliders
    mdSliders = [{'display_text': 'January',
                  'name': 'lc_jan',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_jan'],
                  'step': 0.1},
                 {'display_text': 'February',
                  'name': 'lc_feb',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_feb'],
                  'step': 0.1},
                 {'display_text': 'March',
                  'name': 'lc_mar',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_mar'],
                  'step': 0.1},
                 {'display_text': 'April',
                  'name': 'lc_apr',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_apr'],
                  'step': 0.1},
                 {'display_text': 'May',
                  'name': 'lc_may',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_may'],
                  'step': 0.1},
                 {'display_text': 'June',
                  'name': 'lc_jun',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_jun'],
                  'step': 0.1},
                 {'display_text': 'July',
                  'name': 'lc_jul',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_jul'],
                  'step': 0.1},
                 {'display_text': 'August',
                  'name': 'lc_aug',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_aug'],
                  'step': 0.1},
                 {'display_text': 'September',
                  'name': 'lc_sep',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_sep'],
                  'step': 0.1},
                 {'display_text': 'October',
                  'name': 'lc_oct',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_oct'],
                  'step': 0.1},
                 {'display_text': 'November',
                  'name': 'lc_nov',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_nov'],
                  'step': 0.1},
                 {'display_text': 'December',
                  'name': 'lc_dec',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['lc_dec'],
                  'step': 0.1}]

    ldSliders = [{'display_text': 'January',
                  'name': 'dc_jan',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_jan'],
                  'step': 0.1},
                 {'display_text': 'February',
                  'name': 'dc_feb',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_feb'],
                  'step': 0.1},
                 {'display_text': 'March',
                  'name': 'dc_mar',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_mar'],
                  'step': 0.1},
                 {'display_text': 'April',
                  'name': 'dc_apr',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_apr'],
                  'step': 0.1},
                 {'display_text': 'May',
                  'name': 'dc_may',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_may'],
                  'step': 0.1},
                 {'display_text': 'June',
                  'name': 'dc_jun',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_jun'],
                  'step': 0.1},
                 {'display_text': 'July',
                  'name': 'dc_jul',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_jul'],
                  'step': 0.1},
                 {'display_text': 'August',
                  'name': 'dc_aug',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_aug'],
                  'step': 0.1},
                 {'display_text': 'September',
                  'name': 'dc_sep',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_sep'],
                  'step': 0.1},
                 {'display_text': 'October',
                  'name': 'dc_oct',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_oct'],
                  'step': 0.1},
                 {'display_text': 'November',
                  'name': 'dc_nov',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_nov'],
                  'step': 0.1},
                 {'display_text': 'December',
                  'name': 'dc_dec',
                  'min': 0,
                  'max': 3,
                  'initial': inflow_form_data['dc_dec'],
                  'step': 0.1}]

    # Template context
    context = {'stage': 'inflow',
               'cancel_btn': cancel_btn,
               'back_btn': back_btn,
               'next_btn': next_btn,
               'ldSliders': ldSliders,
               'mdSliders': mdSliders}

    return render(request, 'parleys_creek_management/workflow/inflow.html', context)


def demand(request, scenario_id):
    """
    Controller for the Monthly Demand Rate form
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Handle form
    demand_form_data = a_scenario.demand

    if 'nav_submit' in request.POST:
        a_scenario.demand = dict(demand_form_data.items() + dictize_params(request.POST).items())
        a_scenario.last_updated = datetime.now()
        session.commit()

        # Action of redirect given by value of submit button chosen
        action = request.POST['nav_submit']

        return redirect_to_action(action=action, scenario_id=scenario_id)

    # Nav form action buttons
    cancel_btn = {'buttons': [
        {'display_text': 'Cancel',
         'href': reverse('parleys_creek_management:workflow_cancel', kwargs={'scenario_id': scenario_id})}]
    }

    # Get scenario number
    sc_number = a_scenario.scenario['sc_number']

    # Skip inflow step if scenario is any other type beside historical
    if sc_number == '1':
        back_btn = {'buttons': [
            {'display_text': 'Back',
             'name': 'nav_submit',
             'attributes': 'value=inflow form=input-form',
             'submit': True}
        ]
        }
    else:
        back_btn = {'buttons': [
            {'display_text': 'Back',
             'name': 'nav_submit',
             'attributes': 'value=general form=input-form',
             'submit': True}
        ]
        }

    next_btn = {'buttons': [
        {'display_text': 'Next',
         'name': 'nav_submit',
         'style': 'success',
         'attributes': 'value=summary form=input-form',
         'submit': True}
    ]
    }

    # Form sliders
    demandSliders = [{'display_text': 'January',
                      'name': 'dem_jan',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_jan'],
                      'step': 0.1},
                     {'display_text': 'February',
                      'name': 'dem_feb',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_feb'],
                      'step': 0.1},
                     {'display_text': 'March',
                      'name': 'dem_mar',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_mar'],
                      'step': 0.1},
                     {'display_text': 'April',
                      'name': 'dem_apr',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_apr'],
                      'step': 0.1},
                     {'display_text': 'May',
                      'name': 'dem_may',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_may'],
                      'step': 0.1},
                     {'display_text': 'June',
                      'name': 'dem_jun',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_jun'],
                      'step': 0.1},
                     {'display_text': 'July',
                      'name': 'dem_jul',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_jul'],
                      'step': 0.1},
                     {'display_text': 'August',
                      'name': 'dem_aug',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_aug'],
                      'step': 0.1},
                     {'display_text': 'September',
                      'name': 'dem_sep',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_sep'],
                      'step': 0.1},
                     {'display_text': 'October',
                      'name': 'dem_oct',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_oct'],
                      'step': 0.1},
                     {'display_text': 'November',
                      'name': 'dem_nov',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_nov'],
                      'step': 0.1},
                     {'display_text': 'December',
                      'name': 'dem_dec',
                      'min': 0,
                      'max': 3,
                      'initial': demand_form_data['dem_dec'],
                      'step': 0.1}]

    # Template context
    context = {'stage': 'demand',
               'cancel_btn': cancel_btn,
               'back_btn': back_btn,
               'next_btn': next_btn,
               'demandSliders': demandSliders}

    return render(request, 'parleys_creek_management/workflow/demand.html', context)


def summary(request, scenario_id):
    """
    Controller for the workflow summary page
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    scenario_name = a_scenario.name
    description = a_scenario.description
    general_form_data = a_scenario.general
    inflow_form_data = a_scenario.inflow
    demand_form_data = a_scenario.demand
    scenario_form_data = a_scenario.scenario

    climate_scenario = sc_number_key[scenario_form_data['sc_number']]
    sc_number = scenario_form_data['sc_number']

    if 'summary_submit' in request.POST:
        return redirect_to_action(action=request.POST['summary_submit'], scenario_id=scenario_id)

    # Form action buttons
    delete_btn = {'buttons': [{'display_text': 'Delete',
                               'href': reverse('parleys_creek_management:workflow_cancel',
                                               kwargs={'scenario_id': scenario_id}),
                               'style': 'danger'}]
    }

    clone_btn = {'buttons': [{'display_text': 'Clone',
                              'href': reverse('parleys_creek_management:workflow_clone',
                                              kwargs={'scenario_id': scenario_id}),
                              'style': 'primary'}]
    }

    done_btn = {'buttons': [{'display_text': 'Done',
                             'href': reverse('parleys_creek_management:jobs'),
                             'style': 'success'}]
    }

    # Template context
    context = {'stage': 'summary',
               'scenario_name': scenario_name,
               'description': description,
               'general_form_data': general_form_data,
               'inflow_form_data': inflow_form_data,
               'demand_form_data': demand_form_data,
               'climate_scenario': climate_scenario,
               'sc_number': sc_number,
               'delete_btn': delete_btn,
               'clone_btn': clone_btn,
               'done_btn': done_btn,
    }

    return render(request, 'parleys_creek_management/workflow/summary.html', context)


def clone(request, scenario_id):
    """
    Clone the current scenario and redirect to the beginning of the workflow
    """
    # Get original
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Create clone
    a_clone = a_scenario.clone()
    session.add(a_clone)
    session.commit()
    clone_id = a_clone.id
    session.close()

    return redirect_to_action(action='scenario', scenario_id=clone_id)


def cancel_delete(request, scenario_id):
    """
    Exit the app gracefully on cancel
    """
    # Retrieve the scenario
    session = SessionMaker()
    a_scenario = session.query(ManagementScenario).filter(ManagementScenario.id == scenario_id).one()

    # Delete the current scenario
    session.delete(a_scenario)
    session.commit()
    session.close()

    return redirect('parleys_creek_management:home')


def dictize_params(params):
    """
    Parse parameters into a normal dictionary
    """
    param_dict = dict()
    for key, value in params.iteritems():
        param_dict[key] = value

    return param_dict


def redirect_to_action(action, scenario_id):
    """
    Perform redirect based on action provided
    """
    return redirect('parleys_creek_management:workflow_' + action, scenario_id=scenario_id)