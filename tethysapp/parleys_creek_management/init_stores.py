from model import Base, engine


def init_jobs_database(first_time):
    """
    Initialize the jobs database
    """
    Base.metadata.create_all(engine)

    if first_time:
        pass