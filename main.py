import streamlit as st
import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the Patient table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS Patient (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birthday TEXT NOT NULL,
                    phoneNumber TEXT NOT NULL,
                    visitType TEXT NOT NULL
                )""")

cursor.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  specialty TEXT,
                  phone_number TEXT,
                  email TEXT)''')

# Function to create a new patient
def create_patient(name, birthday, phone_number, visit_type):
    cursor.execute("INSERT INTO Patient (name, birthday, phoneNumber, visitType) VALUES (?, ?, ?, ?)", 
                   (name, birthday, phone_number, visit_type))
    conn.commit()

# Function to read all patients
def read_patients():
    cursor.execute("SELECT * FROM Patient")
    rows = cursor.fetchall()
    return rows

# Function to read a single patient by ID
def read_patient(patient_id):
    cursor.execute("SELECT * FROM Patient WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    return row

# Function to update a patient by ID
def update_patient(patient_id, name, birthday, phone_number, visit_type):
    cursor.execute("UPDATE Patient SET name=?, birthday=?, phoneNumber=?, visitType=? WHERE id=?", 
                   (name, birthday, phone_number, visit_type, patient_id))
    conn.commit()

# Function to delete a patient by ID
def delete_patient(patient_id):
    cursor.execute("DELETE FROM Patient WHERE id=?", (patient_id,))
    conn.commit()

# Function to create a new doctor
def create_doctor(name, type_of_doctor):
    cursor.execute("INSERT INTO Doctor (name, typeOfDoctor) VALUES (?, ?)", (name, type_of_doctor))
    conn.commit()

# Function to read all doctors
def read_doctors():
    cursor.execute("SELECT * FROM Doctor")
    rows = cursor.fetchall()
    return rows

# Function to read a single doctor by ID
def read_doctor(doctor_id):
    cursor.execute("SELECT * FROM Doctor WHERE id=?", (doctor_id,))
    row = cursor.fetchone()
    return row

# Function to update a doctor by ID
def update_doctor(doctor_id, name, type_of_doctor):
    cursor.execute("UPDATE Doctor SET name=?, typeOfDoctor=? WHERE id=?", (name, type_of_doctor, doctor_id))
    conn.commit()

# Function to delete a doctor by ID
def delete_doctor(doctor_id):
    cursor.execute("DELETE FROM Doctor WHERE id=?", (doctor_id,))
    conn.commit()

# Define the Streamlit app
def app():
    # Add a title and header
    st.title('Patient and Doctor Manager')
    st.header('Patients')
    
    # Add a form for creating new patients
    st.subheader('Add a new patient')
    name = st.text_input('Name')
    birthday = st.text_input('Birthday')
    phone_number = st.text_input('Phone number')
    visit_type = st.selectbox('Visit type', ['New patient', 'Follow-up', 'Consultation'])
    if st.button('Create'):
        create_patient(name, birthday, phone_number, visit_type)
        st.success('Patient created!')
    
    # Add a table of all patients
    st.subheader('All patients')
    patients = read_patients()
    if len(patients) > 0:
        for patient in patients:
            st.write(patient)
    else:
        st.warning('No patients found.')
    
    # Add a form for updating an existing patient
    st.subheader('Update a patient')
    patient_id = st.number_input('Patient ID')
    patient = read_patient(patient_id)
    if patient:
        name = st.text_input('Name', patient[1])
        birthday = st.text_input('Birthday', patient[2])
        phone_number = st.text_input('Phone Number', patient[3])

        visit_type = st.selectbox('Visit type', ['New patient', 'Follow-up', 'Consultation'], 
                                  index=0 if patient[4] == 'New patient' else 1 if patient[4] == 'Follow-up' else 2)
        if st.button('Update'):
            update_patient(patient_id, name, birthday, phone_number, visit_type)
            st.success('Patient updated!')
    else:
        st.warning('Patient not found.')
    
    # Add a form for deleting an existing patient
    st.subheader('Delete a patient')
    patient_id = st.number_input('Patient ID')
    if st.button('Delete'):
        delete_patient(patient_id)
        st.success('Patient deleted!')
    
    # Add a header for doctors
    st.header('Doctors')
    
    # Add a form for creating new doctors
    st.subheader('Add a new doctor')
    name = st.text_input('Name')
    type_of_doctor = st.text_input('Type of doctor')
    if st.button('Create'):
        create_doctor(name, type_of_doctor)
        st.success('Doctor created!')
    
    # Add a table of all doctors
    st.subheader('All doctors')
    doctors = read_doctors()
    if len(doctors) > 0:
        for doctor in doctors:
            st.write(doctor)
    else:
        st.warning('No doctors found.')
    
    # Add a form for updating an existing doctor
    st.subheader('Update a doctor')
    doctor_id = st.number_input('Doctor ID')
    doctor = read_doctor(doctor_id)
    if doctor:
        name = st.text_input('Name', doctor[1])
        type_of_doctor = st.text_input('Type of doctor', doctor[2])
        if st.button('Update'):
            update_doctor(doctor_id, name, type_of_doctor)
            st.success('Doctor updated!')
    else:
        st.warning('Doctor not found.')
    
    # Add a form for deleting an existing doctor
    st.subheader('Delete a doctor')
    doctor_id = st.number_input('Doctor ID')
    if st.button('Delete'):
        delete_doctor(doctor_id)
        st.success('Doctor deleted!')

if __name__ == '__main__':
    app()