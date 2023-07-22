from fastapi import FastAPI, HTTPException
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Passenger,Car, Driver, ResetPassword 
from fastapi import Depends
from sqlalchemy.orm import Session
from response import JSONResponse, JSONResponseObject   
from fastapi.responses import Response
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy import and_
import smtp
import pyotp
import smtplib
from email.mime.text import MIMEText

from pydantic import BaseModel
from ViewModel import PassengerViewModel, LoginViewModel , DriverViewModel
from ViewModel import UpdatePassengerProfileSchema, UpdateDriverProfileSchema , ForgotPasswordViewModel , ResetPasswordViewModel
#uvicorn main:app --reload;
#sqlacodegen sqlite:///F:/semester7/FYP_Project/Database/fyp2.db --outfile models.py
app=FastAPI()

database_url = "sqlite:///F:/semester7/FYP_Project/Database/fyp2.db"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#DRIVER SIGNUP API
@app.post("/driversignup")
def driver_signup(driver: DriverViewModel, db: Session = Depends(get_db)):
    
    response = JSONResponse()

    result=db.query(Driver).filter_by(Email=driver.email, CNIC=driver.cnic, EmployeeID=driver.employeeID, Contact=driver.contact).first()
    if result:
        response.StatusCode=500
        response.Message="Passenger Already Exist"
        return response
 
    #code here
    driver_data = Driver(
        Name=driver.name,
        Email=driver.email,
        Contact=driver.contact,
        EmployeeID=driver.employeeID,
        CNIC=driver.cnic,
        Password=driver.password,
        LicenseNum=driver.licenseNum
    )

    db.add(driver_data)
    db.commit()
    db.refresh(driver_data)

    response.StatusCode = 200
    response.Message = "Driver Signup Successful"
    #response.Object = driver_data
    return response


#DRIVER LOGIN API
@app.post("/driverlogin")
def driver_login(loginView: LoginViewModel, db: Session = Depends(get_db)):
    response = JSONResponse()

    driver = db.query(Driver).filter_by(EmployeeID=loginView.employeeID).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    if driver.Password != loginView.password:
        raise HTTPException(status_code=401,detail="Invalid password")

    response.StatusCode = 200
    response.Message = "Driver Login Successful"
    return response


#GET DRIVER PROFILE  API
@app.get("/driver/{employeeid}")
def driver_details(employeeid, db: Session = Depends(get_db)):
    response = JSONResponseObject()
    data = db.query(Driver).filter_by(EmployeeID=employeeid).first()

    if not data:
        raise HTTPException(status_code=404, detail="Driver not found")
          
    response.StatusCode = 200
    response.Message = "Driver Found"
    response.Object = data
    return response


@app.put("/driverupdate/{employeeid}")
def update_driver_profile(employeeid: str, profile: UpdateDriverProfileSchema, db: Session = Depends(get_db)):
    response = JSONResponse()
    driver = db.query(Driver).filter_by(EmployeeID=employeeid).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    # Check if the email already belongs to another user
    existing_driver = db.query(Driver).filter(and_(Driver.Email == profile.email, Driver.EmployeeID != employeeid)).first()
    if existing_driver:
        raise HTTPException(status_code=400, detail="Email already belongs to another user")

    # Update driver's profile with the provided information
    driver.Name = profile.name
    driver.Email = profile.email 
    driver.Contact = profile.contact
    driver.CNIC = profile.cnic
    driver.LicenseNum = profile.license_number

    db.commit()      

    response.StatusCode = 200
    response.Message = "Driver profile updated successfully"
   # response.Object = driver
    return response



#PASSENGER LOGIN API
@app.post("/passengerlogin")
def passenger_login(loginView: LoginViewModel, db: Session = Depends(get_db)):
    response = JSONResponse()

    passenger = db.query(Passenger).filter_by(EmployeeID=loginView.employeeID).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    if passenger.Password != loginView.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    response.StatusCode = 200
    response.Message = "Passenger Login Successful"
    return response


@app.get('/car')
def get_car(db: Session = Depends(get_db)):
    data = db.query(Car).all()
    return data


#PASSENGER SIGNUP API
@app.post("/signup")
def passenger_signup(passenger: PassengerViewModel, db: Session = Depends(get_db)):
    
    response = JSONResponse()

    result=db.query(Passenger).filter_by(Email=passenger.email, CNIC=passenger.cnic, EmployeeID=passenger.employeeID, Contact=passenger.contact).first()
    if result:
        response.StatusCode=500
        response.Message="Passenger Already Exist"
        return response
 
    #code here
    passenger_data = Passenger(
        Name=passenger.name,
        Email=passenger.email,
        Contact=passenger.contact,
        EmployeeID=passenger.employeeID,
        CNIC=passenger.cnic,
        Password=passenger.password
    )

    db.add(passenger_data)
    db.commit()
    db.refresh(passenger_data)

    response.StatusCode = 200
    response.Message = "Passenger Signup Successful"
    #response.Object = passenger_data
    return response


#GET PASSENGER PROFILE  API
@app.get("/passenger/{employeeid}")
def passenger_details(employeeid, db: Session = Depends(get_db)):
    response = JSONResponseObject()
    data = db.query(Passenger).filter_by(EmployeeID=employeeid).first()

    if not data:
        raise HTTPException(status_code=404, detail="Passenger not found")
          
    response.StatusCode = 200
    response.Message = "Passenger Found"
    response.Object = data
    return response

#UPDTAE PASSENGER PROFILE

@app.put("/passengerupdate/{employeeid}")
def update_passenger_profile(employeeid: str, profile: UpdatePassengerProfileSchema, db: Session = Depends(get_db)):
    response = JSONResponse()
    passenger = db.query(Passenger).filter_by(EmployeeID=employeeid).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
     # Check if the email already belongs to another user
    existing_passenger = db.query(Passenger).filter(and_(Passenger.Email == profile.email, Passenger.EmployeeID != employeeid)).first()
    if existing_passenger:
        raise HTTPException(status_code=400, detail="Email already belongs to another user")


    # Update passenger's profile with the provided information
    passenger.Name = profile.name
    passenger.Email = profile.email 
    passenger.Contact = profile.contact
    passenger.CNIC = profile.cnic

    db.commit()      

    response.StatusCode = 200
    response.Message = "Passenger profile updated successfully"
    #response.Object = passenger
    return response

@app.post('/forget-password')   
def forget_password(request: ForgotPasswordViewModel,  db: Session = Depends(get_db)):
    try:
        email = request.email
        otp = str(random.randint(100000, 999999))
        if request.type == "Passenger":
            passenger = db.query(Passenger).filter_by(Email = email).one()   
            reset_password = db.query(ResetPassword).filter_by(PassengerID= passenger.PassengerID).first()
            if not reset_password:
                resetpassword = ResetPassword()
                resetpassword.PassengerID = passenger.PassengerID
                resetpassword.OTP = otp
                db.add(resetpassword)
                db.commit()
                db.refresh(resetpassword)
            else:
                reset_password.OTP = otp    
                db.add(reset_password)
                db.commit()

        #smtp.sendEmail(email, otp)
        return {'message': 'OTP sent to your email. Please check your inbox.'}
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Email not found.')

@app.post('/reset-password')   
def reset_password(request: ResetPasswordViewModel,  db: Session = Depends(get_db)):
    try:
        email = request.email
        otp = request.otp
        newPass = request.new_password
        if request.type == "Passenger":
            passengerRow = db.query(Passenger).filter_by(Email=email).first()
            resetPasswordRow = db.query(ResetPassword).filter_by(PassengerID = passengerRow.PassengerID).first()
            if resetPasswordRow.OTP == otp:
                print("OTP matched")
                passengerRow.Password = newPass
                db.add(passengerRow)
                db.commit()
                return {'message': 'password updated successfully'}
                #db.refresh(passengerRow)
            else:
                return {'message': 'invalid OTP'}
            
    except NoResultFound:
        raise HTTPException(status_code=404,detail='Passenger not found')
    except Exception as e:
        raise HTTPException(status_code=500,detail='An error occurred')


@app.get('/check')
async def hello(): 
    return {'example': 'This is an example', 'data': 0}

