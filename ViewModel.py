from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional


class UpdatePassengerProfileSchema(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    contact: Optional[str]
    cnic: Optional[str]
    

class UpdateDriverProfileSchema(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    contact: Optional[str]
    cnic: Optional[str]
    license_number: Optional[str]
    

class PassengerViewModel(BaseModel):
    name: str
    email: str
    contact: str
    employeeID: str
    cnic: str
    password: str

class LoginViewModel(BaseModel):
    employeeID: str
    password: str


class DriverViewModel(BaseModel):
    name: str
    email: str
    contact: str
    employeeID: str
    cnic: str
    password: str
    licenseNum: str


class ForgotPasswordViewModel(BaseModel):
    email: str
    type: str

class ResetPasswordViewModel(BaseModel):
    email: str
    otp: str
    new_password: str
    type: str
