
from flask import Flask, g
from flask import render_template

from sqlalchemy import (create_engine, Column, Integer, String, 
                        ForeignKey, and_)
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


#------------------------------------------------------------------------------
###############################################################################
class Job(Base):
    """
    """
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    job_title = Column(String(120), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False)
    job_locations = relationship("JobLocation", cascade="all, delete-orphan", 
                        backref='jobs')

    def __init__(self, job_title, category, status):
        """
        """
        self.job_title = job_title
        self.category = category
        self.status = status

    def __repr__(self):
        """
        """
        return '<(%r, %r, %r)>' % (
            self.job_title, self.category, self.status
        )

###############################################################################
class Location(Base):
    """
    """
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    location = Column(String(30), nullable=False)

    def __init__(self, location):
        """
        """
        self.location = location

    def __repr__(self):
        """
        """
        return '<Location %r>' % self.location

###############################################################################
class JobLocation(Base):
    __tablename__ = 'jobs_locations'
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True)

    def __init__(self, job_id, location_id):
        self.job_id = job_id
        self.location_id = location_id
    location = relationship(Location, lazy='joined')

###############################################################################
#------------------------------------------------------------------------------


if __name__ == '__main__':
    # psycopg2
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/jobs',
                         echo=True)
    Base.metadata.create_all(bind=engine)

 
    Session = sessionmaker(bind=engine)
    session = Session()   


##    # query the job, print job description
##    jobs = session.query(Job).filter_by(status='Fixed-term').all()
##    for job in jobs:
##        print(job)


##    # print jobs based on location Mountain View
##    q = session.query(Job).join('job_locations', 'location')
##    q = q.filter(and_(Location.location == 'Mountain View'))
##
##    print([job.job_title for job in q])




    app = Flask(__name__)
    app.debug = True


    @app.before_request
    def create_session():
        g.session = Session()


    @app.route('/')
    def index():
        return '<h1 style="color: red">API Endpoint</h1>'


    @app.route('/jobs/')
    def jobs():
        jobs = g.session.query(Job).all()

        return render_template('jobs.html', jobs=jobs)


    @app.route('/jobs/<location>')
    def jobs_by_location(location):
        jobs_by_location = g.session.query(Job).join('job_locations',
                                                     'location').filter_by(location=location)

        return render_template('jobs_by_location.html', jobs_by_location=jobs_by_location, location=location)


    app.run()

