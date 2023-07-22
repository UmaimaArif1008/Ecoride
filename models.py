# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'Admin'

    AdminID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Password = Column(Text)


class Car(Base):
    __tablename__ = 'Car'

    CarID = Column(Integer, primary_key=True)
    CarNum = Column(Text)
    Model = Column(Integer)
    CarPic = Column(LargeBinary)
    CarColor = Column(Text)
    DriverID = Column(Integer)


class Driver(Base):
    __tablename__ = 'Driver'

    DriverID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Email = Column(Text)
    Contact = Column(Text)
    EmployeeID = Column(Text)
    CNIC = Column(Text)
    Password = Column(Text)
    LicenseNum = Column(Text)


class Passenger(Base):
    __tablename__ = 'Passenger'

    PassengerID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Email = Column(Text)
    Contact = Column(Text)
    EmployeeID = Column(Text)
    CNIC = Column(Text)
    Password = Column(Text)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class ResetPassword(Base):
    __tablename__ = 'ResetPassword'

    RestID = Column(Integer, primary_key=True)
    OTP = Column(Text)
    PassengerID = Column(ForeignKey('Passenger.PassengerID'))

    Passenger = relationship('Passenger')
