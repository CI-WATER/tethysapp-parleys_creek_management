import collections
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy.orm import sessionmaker

from utilities import get_persistent_store_engine

# DB Engine, sessionmaker and base
def get_session_maker():
    engine = get_persistent_store_engine('jobs_database')
    return sessionmaker(bind=engine)

Base = declarative_base()

LITTLE_DELL_VOLUME = 'little-dell-volume'
LITTLE_DELL_RELEASE = 'little-dell-release'
LITTLE_DELL_SPILL = 'little-dell-spill'
MOUNTAIN_DELL_VOLUME = 'mountain-dell-volume'
MOUNTAIN_DELL_RELEASE = 'mountain-dell-release'
MOUNTAIN_DELL_SPILL = 'mountain-dell-spill'
DELL_CREEK_INFLOW = 'dell-creek-inflow'
LAMBS_CREEK_INFLOW = 'lambs-creek-inflow'
RELIABILITY = 'reliability'


class ManagementScenario(Base):
    """
    ORM for storing scenario information
    """
    __tablename__ = 'parleys_creek_scenarios'
    
    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    percentage = Column(Integer)
    user_id = Column(String)
    created = Column(DateTime)
    last_updated = Column(DateTime)
    general = Column(PickleType)
    inflow = Column(PickleType)
    demand = Column(PickleType)
    scenario = Column(PickleType)
    job_status = Column(String)
    results_link = Column(String)
    little_dell_volume = Column(PickleType)
    little_dell_release = Column(PickleType)
    little_dell_spill = Column(PickleType)
    mountain_dell_volume = Column(PickleType)
    mountain_dell_release = Column(PickleType)
    mountain_dell_spill = Column(PickleType)
    dell_creek_inflow = Column(PickleType)
    lambs_creek_inflow = Column(PickleType)
    reliability = Column(PickleType)
    
    def __init__(self, name, user_id):
        """
        Create a new scenario with all the defaults set
        """
        # Name and ID
        self.name = name
        self.description = ''
        self.percentage = 0
        self.user_id = user_id
        
        # Set times
        now = datetime.now()
        self.created = now
        self.last_updated = now
        
        # Set defaults for form defaults
        general_form_defaults = {'capacity_mt': '3200',
                                 'init_mt': '2000',
                                 'deadpool_mt': '800',
                                 'capacity_lit': '20000',
                                 'init_lit': '5700',
                                 'deadpool_lit': '0'}
        
        self.general = general_form_defaults
        
        inflow_form_defaults = {'dc_jan': '1',
                                'dc_feb': '1',
                                'dc_mar': '1',
                                'dc_apr': '1',
                                'dc_may': '1',
                                'dc_jun': '1',
                                'dc_jul': '1',
                                'dc_aug': '1',
                                'dc_sep': '1',
                                'dc_oct': '1',
                                'dc_nov': '1',
                                'dc_dec': '1',
                                'lc_jan': '1',
                                'lc_feb': '1',
                                'lc_mar': '1',
                                'lc_apr': '1',
                                'lc_may': '1',
                                'lc_jun': '1',
                                'lc_jul': '1',
                                'lc_aug': '1',
                                'lc_sep': '1',
                                'lc_oct': '1',
                                'lc_nov': '1',
                                'lc_dec': '1'}
        
        self.inflow = inflow_form_defaults
        
        demand_form_defaults = {'dem_jan': '1',
                                'dem_feb': '1',
                                'dem_mar': '1',
                                'dem_apr': '1',
                                'dem_may': '1',
                                'dem_jun': '1',
                                'dem_jul': '1',
                                'dem_aug': '1',
                                'dem_sep': '1',
                                'dem_oct': '1',
                                'dem_nov': '1',
                                'dem_dec': '1',
                                'mks_jan': '1',
                                'mks_feb': '1',
                                'mks_mar': '1',
                                'mks_apr': '1',
                                'mks_may': '1',
                                'mks_jun': '1',
                                'mks_jul': '1',
                                'mks_aug': '1',
                                'mks_sep': '1',
                                'mks_oct': '1',
                                'mks_nov': '1',
                                'mks_dec': '1'}
        
        self.demand = demand_form_defaults
        
        scenario_form_defaults = {'sc_number': '1'}
        
        self.scenario = scenario_form_defaults
        
        # Default job status
        self.job_status = 'pending'
        
    def get_web_service_inputs(self):
        """
        Combine all inputs to the goldsim web service into one dictionary
        """
        
        one_dict = dict(self.general.items() +
                        self.inflow.items() +
                        self.demand.items() +
                        self.scenario.items())
        
        return self.convert(one_dict)

    def convert(self, data):
        """
        Conversion function from stack overflow
        http://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
        """
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.convert, data))
        else:
            return data
        
    def clone(self):
        """
        Returns a new management scenario that is a copy of this one
        """
        copy_name = 'Clone of ' + self.name
        
        # Create new management scenario
        copy_scenario = ManagementScenario(copy_name, self.user_id)
        
        # Copy information into the copy
        copy_scenario.general = self.general
        copy_scenario.inflow = self.inflow
        copy_scenario.demand = self.demand
        copy_scenario.scenario = self.scenario
        
        return copy_scenario
    
    def set_results(self, results):
        """
        Set all results properties
        """
        self.little_dell_volume = results[LITTLE_DELL_VOLUME]
        self.little_dell_release = results[LITTLE_DELL_RELEASE]
        self.little_dell_spill = results[LITTLE_DELL_SPILL]
        self.mountain_dell_volume = results[MOUNTAIN_DELL_VOLUME]
        self.mountain_dell_release = results[MOUNTAIN_DELL_RELEASE]
        self.mountain_dell_spill = results[MOUNTAIN_DELL_SPILL]
        self.dell_creek_inflow = results[DELL_CREEK_INFLOW]
        self.lambs_creek_inflow = results[LAMBS_CREEK_INFLOW]
        self.reliability = results[RELIABILITY]
    
    @classmethod   
    def get_results_dataset(cls, scenario_id, plot_name):
        """
        Return the appropriate dataset
        """
        SessionMaker = get_session_maker()
        session = SessionMaker()
        
        if plot_name == LITTLE_DELL_VOLUME:
            result = session.query(cls.little_dell_volume).filter(cls.id == scenario_id).one()
            return result.little_dell_volume
        
        if plot_name == LITTLE_DELL_RELEASE:
            result = session.query(cls.little_dell_release).filter(cls.id == scenario_id).one()
            return result.little_dell_release
        
        if plot_name == LITTLE_DELL_SPILL:
            result = session.query(cls.little_dell_spill).filter(cls.id == scenario_id).one()
            return result.little_dell_spill
        
        if plot_name == MOUNTAIN_DELL_VOLUME:
            result = session.query(cls.mountain_dell_volume).filter(cls.id == scenario_id).one()
            return result.mountain_dell_volume
        
        if plot_name == MOUNTAIN_DELL_RELEASE:
            result = session.query(cls.mountain_dell_release).filter(cls.id == scenario_id).one()
            return result.mountain_dell_release
        
        if plot_name == MOUNTAIN_DELL_SPILL:
            result = session.query(cls.mountain_dell_spill).filter(cls.id == scenario_id).one()
            return result.mountain_dell_spill
        
        if plot_name == DELL_CREEK_INFLOW:
            result = session.query(cls.dell_creek_inflow).filter(cls.id == scenario_id).one()
            return result.dell_creek_inflow
        
        if plot_name == LAMBS_CREEK_INFLOW:
            result = session.query(cls.lambs_creek_inflow).filter(cls.id == scenario_id).one()
            return result.lambs_creek_inflow
