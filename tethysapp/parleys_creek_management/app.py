from tethys_apps.base import TethysAppBase, url_map_maker, PersistentStore


class ParleysCreekManagementTool(TethysAppBase):
    """
    Tethys app class for Parleys Creek Management Tool.
    """

    name = 'Parleys Creek Management Tool'
    index = 'parleys_creek_management:home'
    icon = 'parleys_creek_management/images/icon.gif'
    package = 'parleys_creek_management'
    root_url = 'parleys-creek-management'
    color = '#915E40'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='parleys-creek-management',
                           controller='parleys_creek_management.controllers.root.home'),
                    UrlMap(name='workflow_new',
                           url='parleys-creek-management/new',
                           controller='parleys_creek_management.controllers.workflow.new'),
                    UrlMap(name='workflow_scenario',
                           url='parleys-creek-management/{scenario_id}/scenario',
                           controller='parleys_creek_management.controllers.workflow.scenario'),
                    UrlMap(name='workflow_general',
                           url='parleys-creek-management/{scenario_id}/general',
                           controller='parleys_creek_management.controllers.workflow.general'),
                    UrlMap(name='workflow_inflow',
                           url='parleys-creek-management/{scenario_id}/inflow',
                           controller='parleys_creek_management.controllers.workflow.inflow'),
                    UrlMap(name='workflow_demand',
                           url='parleys-creek-management/{scenario_id}/demand',
                           controller='parleys_creek_management.controllers.workflow.demand'),
                    UrlMap(name='workflow_summary',
                           url='parleys-creek-management/{scenario_id}/summary',
                           controller='parleys_creek_management.controllers.workflow.summary'),
                    UrlMap(name='workflow_clone',
                           url='parleys-creek-management/{scenario_id}/clone',
                           controller='parleys_creek_management.controllers.workflow.clone'),
                    UrlMap(name='workflow_cancel',
                           url='parleys-creek-management/{scenario_id}/cancel',
                           controller='parleys_creek_management.controllers.workflow.cancel_delete'),
                    UrlMap(name='jobs',
                           url='parleys-creek-management/jobs',
                           controller='parleys_creek_management.controllers.jobs.jobs'),
                    UrlMap(name='jobs_delete',
                           url='parleys-creek-management/jobs/{scenario_id}/delete',
                           controller='parleys_creek_management.controllers.jobs.delete'),
                    UrlMap(name='jobs_status',
                           url='parleys-creek-management/jobs/{scenario_id}/status',
                           controller='parleys_creek_management.controllers.jobs.status'),
                    UrlMap(name='jobs_run',
                           url='parleys-creek-management/jobs/{scenario_id}/run',
                           controller='parleys_creek_management.controllers.jobs.run'),
                    UrlMap(name='results_view',
                           url='parleys-creek-management/results/{scenario_id}/{plot_name}/view',
                           controller='parleys_creek_management.controllers.results.view')
        )

        return url_maps

    def persistent_stores(self):
        """
        Persistent stores
        """
        persistent_stores = (PersistentStore(name='jobs_database',
                                             initializer='init_stores.init_jobs_database'),)

        return persistent_stores