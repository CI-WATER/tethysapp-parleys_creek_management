from ckanext.tethys_apps.lib.app_base import AppBase


class ParleysCreekManagementModelApp(AppBase):
    '''
    Example implementation of an app
    '''

    def registerApp(self, app):
        '''
        Register the app
        '''

        app.addApp(name='Parleys Creek Management Tool',
                   index='pcmt-root',
                   icon='ckanapp/parleys_creek_management/images/icon.gif')


    def registerControllers(self, controllers):
        '''
        Add controllers
        '''

        controllers.addController(name='pcmt-root',
                                  url='parleys-creek-management-tool',
                                  controller='parleys_creek_management.controllers.root:RootController',
                                  action='index')

        controllers.addController(name='pcmt-new-scenario',
                                  url='parleys-creek-management-tool/new',
                                  controller='parleys_creek_management.controllers.workflow:WorkflowController',
                                  action='new')

        controllers.addController(name='pcmt-workflow',
                                  url='parleys-creek-management-tool/{id}/{action}',
                                  controller='parleys_creek_management.controllers.workflow:WorkflowController')

        controllers.addController(name='pcmt-jobs',
                                  url='parleys-creek-management-tool/jobs',
                                  controller='parleys_creek_management.controllers.jobs:JobsController',
                                  action='jobs')

        controllers.addController(name='pcmt-jobs-action',
                                  url='parleys-creek-management-tool/jobs/{id}/{action}',
                                  controller='parleys_creek_management.controllers.jobs:JobsController')

        controllers.addController(name='pcmt-results-plot',
                                  url='parleys-creek-management-tool/results/{id}/{plot_name}/{action}',
                                  controller='parleys_creek_management.controllers.results:ResultsController')


    def registerTemplateDirectories(self, templateDirs):
        '''
        Add template directories
        '''

        templateDirs.addTemplateDirectory(directory='parleys_creek_management/templates')


    def registerPublicDirectories(self, publicDirs):
        '''
        Add public directories
        '''

        publicDirs.addPublicDirectory(directory='parleys_creek_management/public')


    def registerResources(self, staticDirs):
        '''
        Add static directories
    	'''

        staticDirs.addResource(directory='parleys_creek_management/public/ckanapp/parleys_creek_management',
                               name='ckanapp_parleys_creek_management')


    def registerPersistentStores(self, persistentStores):
        '''
        Add one or more persistent stores
        '''
        persistentStores.addPersistentStore('jobs_database')
        persistentStores.addInitializationScript('parleys_creek_management.lib.init_db')
