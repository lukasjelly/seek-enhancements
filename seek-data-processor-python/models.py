# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Advertiser(Base):
    __tablename__ = 'Advertiser'

    advertiser_Id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    is_verified = Column(TINYINT(1))
    registration_date = Column(DateTime)
    date_added = Column(DateTime)


class Classification(Base):
    __tablename__ = 'Classification'

    classification_Id = Column(INTEGER(11), primary_key=True)
    label = Column(String(255), nullable=False)


class Location(Base):
    __tablename__ = 'Location'

    location_Id = Column(INTEGER(11), primary_key=True)
    area = Column(String(255))
    location = Column(String(255))


class WorkType(Base):
    __tablename__ = 'WorkType'

    work_type_Id = Column(INTEGER(11), primary_key=True)
    label = Column(String(255), nullable=False)


class SubClassification(Base):
    __tablename__ = 'SubClassification'

    subClassification_Id = Column(INTEGER(11), primary_key=True)
    classification_Id = Column(ForeignKey('Classification.classification_Id'), nullable=False, index=True)
    label = Column(String(255), nullable=False)

    Classification = relationship('Classification')


class Job(Base):
    __tablename__ = 'Job'

    job_Id = Column(INTEGER(11), primary_key=True)
    advertiser_Id = Column(ForeignKey('Advertiser.advertiser_Id'), nullable=False, index=True)
    classification_Id = Column(ForeignKey('Classification.classification_Id'), nullable=False, index=True)
    subClassification_Id = Column(ForeignKey('SubClassification.subClassification_Id'), nullable=False, index=True)
    work_type_Id = Column(ForeignKey('WorkType.work_type_Id'), nullable=False, index=True)
    title = Column(String(255))
    phone_number = Column(String(20))
    is_expired = Column(TINYINT(1))
    expires_at = Column(DateTime)
    is_link_out = Column(TINYINT(1))
    is_verified = Column(TINYINT(1))
    abstract = Column(Text)
    content = Column(Text)
    status = Column(String(50))
    listed_at = Column(DateTime)
    salary = Column(String(255))
    share_link = Column(String(255))
    date_added = Column(DateTime)
    bullets = Column(Text)
    questions = Column(Text)

    Advertiser = relationship('Advertiser')
    Classification = relationship('Classification')
    SubClassification = relationship('SubClassification')
    WorkType = relationship('WorkType')


class JobLocation(Base):
    __tablename__ = 'JobLocation'

    job_location_Id = Column(INTEGER(11), primary_key=True)
    job_Id = Column(ForeignKey('Job.job_Id'), nullable=False, index=True)
    location_Id = Column(ForeignKey('Location.location_Id'), nullable=False, index=True)

    Job = relationship('Job')
    Location = relationship('Location')
