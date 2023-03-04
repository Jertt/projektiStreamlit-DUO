import streamlit as st
import sqlite3
import datetime

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create the patients table
c.execute('''CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                fullName TEXT,
                birthday TEXT,
                phoneNumber TEXT,
                visitType TEXT
            )''')

# Create the doctors table
c.execute('''CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                speciality TEXT,
                phoneNumber TEXT,
                email TEXT
            )''')

# Define the functions for creating, reading, updating, and deleting patients
def create_patient(fullName, birthday, phoneNumber, visitType):
    c.execute("INSERT INTO patients (fullName, birthday, phoneNumber, visitType) VALUES (?, ?, ?, ?)", (fullName, birthday, phoneNumber, visitType))
    conn.commit()
    st.success("Patient created: {}".format(fullName))

def read_patients():
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    return patients

def update_patient(id, fullName, birthday, phoneNumber, visitType):
    c.execute("UPDATE patients SET fullName = ?, birthday = ?, phoneNumber = ?, visitType = ? WHERE id = ?", (fullName, birthday, phoneNumber, visitType, id))
    conn.commit()
    st.success("Patient updated: {}".format(fullName))

def delete_patient(id):
    c.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    st.warning("Patient deleted")

# Define the functions for creating, reading, updating, and deleting doctors
def create_doctor(name, speciality, phoneNumber, email):
    c.execute("INSERT INTO doctors (name, speciality, phoneNumber, email) VALUES (?, ?, ?, ?)", (name, speciality, phoneNumber, email))
    conn.commit()
    st.success("Doctor created: {}".format(name))

def read_doctors():
    c.execute("SELECT * FROM doctors")
    doctors = c.fetchall()
    return doctors

def update_doctor(id, name, speciality, phoneNumber, email):
    c.execute("UPDATE doctors SET name = ?, speciality = ?, phoneNumber = ?, email = ? WHERE id = ?", (name, speciality, phoneNumber, email, id))
    conn.commit()
    st.success("Doctor updated: {}".format(name))

def delete_doctor(id):
    c.execute("DELETE FROM doctors WHERE id = ?", (id,))
    conn.commit()
    st.warning("Doctor deleted")

# Define the main function
def main():
    st.set_page_config(page_title="CRUD App", page_icon="👨‍⚕️", layout="wide")

    # Create the sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Patients", "Doctors"))

    # Show the appropriate page based on the user's choice
    if page == "Patients":
        st.title("Patients")

        # Show the form for adding a new patient
        st.subheader("Add a new patient")
        fullName = st.text_input("Full name")
        birthday = st.date_input("Birthday", key='add_birthday')
        phoneNumber = st.text_input("Phone number")
        visitType = st.selectbox("Visit type", ("Check-up", "Consultation", "Procedure", "Lab test"), index=0, key="unique_key_one")
        if st.button("Add"):
            create_patient(fullName, birthday, phoneNumber, visitType)
            st.success("Patient added")

        # Show the table of existing patients
        st.subheader("Patients list")
        patients = read_patients()
        if patients:
            for patient in patients:
                st.write(patient)


        # Show the form for updating a patient
        st.subheader("Update a patient")
        patient_id = st.number_input("Enter the ID of the patient you want to update")
        patient = [p for p in patients if p[0] == patient_id]
        if patient:
            patient = patient[0]
            fullName = st.text_input("Full name", patient[1])
            birthday = st.date_input("Birthday", datetime.datetime.strptime(patient[2], "%Y-%m-%d").date(), key='update_birthday')
            phoneNumber = st.text_input("Phone number", patient[3])
            visitType = st.selectbox("Visit type", ("Check-up", "Consultation", "Procedure", "Lab test"), index=["Check-up", "Consultation", "Procedure", "Lab test"].index(patient[4]), key="unique_key_two")
            if st.button("Update"):
                update_patient(patient_id, fullName, birthday, phoneNumber, visitType)
        else:
            st.warning("Patient not found")

        # Show the form for deleting a patient
        st.subheader("Delete a patient")
        patient_id = st.number_input("Enter the ID of the patient you want to delete")
        if st.button("Delete"):
            delete_patient(patient_id)

    elif page == "Doctors":
        st.title("Doctors")

        # Show the form for adding a new doctor
        st.subheader("Add a new doctor")
        name = st.text_input("Name")
        speciality = st.text_input("Speciality")
        phoneNumber = st.text_input("Phone number")
        email = st.text_input("Email")
        if st.button("Add"):
            create_doctor(name, speciality, phoneNumber, email)

        # Show the table of existing doctors
        st.subheader("Doctors list")
        doctors = read_doctors()
        if doctors:
            for doctor in doctors:
                st.write(doctor)

        # Show the form for updating a doctor
        st.subheader("Update a doctor")
        doctor_id = st.number_input("Enter the ID of the doctor you want to update")
        doctor = [d for d in doctors if d[0] == doctor_id]
        if doctor:
            doctor = doctor[0]
            name = st.text_input("Name", doctor[1])
            speciality = st.text_input("Speciality", doctor[2])
            phoneNumber = st.text_input("Phone number", doctor[3])
            email = st.text_input("Email", doctor[4])
            if st.button("Update"):
                update_doctor(doctor_id, name, speciality, phoneNumber, email)
        else:
            st.warning("Doctor not found")

        # Show the form for deleting a doctor
        st.subheader("Delete a doctor")
        doctor_id = st.number_input("Enter the ID of the doctor you want to delete")
        if st.button("Delete"):
            delete_doctor(doctor_id)

    # Close the database connection
    conn.close()
if __name__ == "__main__":
    main()

