# API Test JSON Objects

This repository contains JSON objects used for testing the API.

## Doctor's Profile


{
    "username": "jdoe123",
    "first_name": "John",
    "last_name": "Doe",
    "email": "jdoe@example.com",
    "password": "SuperSecurePassword123!",
    "date_of_birth": "1980-05-12",
    "gender": "male",
    "address": "123 Medical St, Health City",
    "phone_number": "1234567890",
    "image": null,
    "user_type": "doctors",
    "specialty": "Cardiology",
    "years_experience": 10
}

## Patient's Profile

{
    "username": "patient123",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "password": "securepassword",
    "date_of_birth": "1985-07-20",
    "gender": "male",
    "address": "456 Elm St",
    "phone_number": "0987654321",
    "image": null,
    "user_type": "patients",
    "doctor": "jdoe123",  
    "nurse": "nurse123"
}

## Nurse's Profile

{
    "username": "nurse123",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "password": "securepassword",
    "date_of_birth": "1990-05-15",
    "gender": "female",
    "address": "123 Main St",
    "phone_number": "1234567890",
    "image": null,
    "user_type": "nurses",
    "categoria": "licenciada"
}

## ClinicHistory

{
  "last_modified": "2024-06-18T12:00:00Z",
  "treatments": "Initial Treatment",
  "diseases": "Initial Diseases",
  "doctor": "doctor_username",
  "nurse": "nurse_username",
  "patient": "patient_username"
}


## Appointments

{
  "consultation_date": "2024-06-18T10:00:00",  
  "reason_of_visit": "Check-up",               
  "symptoms": "Headache and fatigue",          
  "diagnosis": "Mild flu",                    
  "prescribed_treatament": "Rest and fluids",  
  "observation": "Monitor closely",            
  "test_conducted": "None",                    
  "patient": "username_del_paciente",          
  "doctor": "username_del_doctor"              
}
