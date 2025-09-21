import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

# Output directory
OUTPUT_DIR = "./data/bronze"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Configuration (row counts) ---
NUM_PATIENTS = 200
NUM_PROVIDERS = 50
NUM_LOCATIONS = 10
NUM_ENCOUNTERS = 1000
NUM_DIAGNOSES = 2500
NUM_PROCEDURES = 1500
NUM_LABS = 5000
NUM_VITALS = 8000
NUM_MEDICATIONS = 2000
NUM_CLAIMS = 1200
NUM_PAYERS = 10
NUM_DEVICES = 50

# --- Helper functions ---
def random_date(start_days_ago=365, end_days_ago=0):
    start_date = datetime.today() - timedelta(days=start_days_ago)
    end_date = datetime.today() - timedelta(days=end_days_ago)
    return fake.date_between(start_date=start_date, end_date=end_date)

# --- Patients ---
patients = []
for i in range(1, NUM_PATIENTS + 1):
    patients.append([
        i,
        fake.first_name(),
        fake.last_name(),
        fake.date_of_birth(minimum_age=0, maximum_age=90),
        random.choice(["M", "F"]),
        fake.phone_number(),
        fake.email(),
        fake.street_address(),
        fake.city(),
        fake.state_abbr(),
        fake.postcode(),
        random.choice(["Epic", "Cerner", "Allscripts"])
    ])

patients_df = pd.DataFrame(patients, columns=[
    "PatientId", "FirstName", "LastName", "DOB", "Gender", "Phone", "Email",
    "AddressLine1", "City", "State", "PostalCode", "SourceSystem"
])
patients_df.to_csv(f"{OUTPUT_DIR}/patients.csv", index=False)

# --- Providers ---
specialties = ["Cardiology", "Oncology", "Pediatrics", "Family Medicine", "Orthopedics", "Psychiatry"]
providers = []
for i in range(1, NUM_PROVIDERS + 1):
    providers.append([
        i,
        fake.first_name(),
        fake.last_name(),
        fake.unique.random_number(digits=10),
        random.choice(specialties),
        fake.company(),
        random.randint(1, NUM_LOCATIONS)
    ])

providers_df = pd.DataFrame(providers, columns=[
    "ProviderId", "FirstName", "LastName", "NPI", "Specialty", "Organization", "LocationId"
])
providers_df.to_csv(f"{OUTPUT_DIR}/providers.csv", index=False)

# --- Locations ---
locations = []
for i in range(1, NUM_LOCATIONS + 1):
    locations.append([
        i,
        f"{fake.city()} Medical Center",
        fake.street_address(),
        fake.city(),
        fake.state_abbr(),
        fake.postcode(),
        random.choice(["East", "West", "North", "South"])
    ])

locations_df = pd.DataFrame(locations, columns=[
    "LocationId", "LocationName", "AddressLine1", "City", "State", "PostalCode", "Region"
])
locations_df.to_csv(f"{OUTPUT_DIR}/locations.csv", index=False)

# --- Encounters ---
encounters = []
for i in range(1, NUM_ENCOUNTERS + 1):
    pid = random.randint(1, NUM_PATIENTS)
    prvid = random.randint(1, NUM_PROVIDERS)
    locid = random.randint(1, NUM_LOCATIONS)
    start_date = random_date(365, 30)
    length = random.randint(0, 10)
    encounters.append([
        i, pid, prvid, locid, start_date,
        random.choice(["Inpatient", "Outpatient", "ER", "Telehealth"]),
        start_date + timedelta(days=length) if length > 0 else None,
        length
    ])

encounters_df = pd.DataFrame(encounters, columns=[
    "EncounterId", "PatientId", "ProviderId", "LocationId", "EncounterDate",
    "EncounterType", "DischargeDate", "LengthOfStay"
])
encounters_df.to_csv(f"{OUTPUT_DIR}/encounters.csv", index=False)

# --- Diagnoses ---
icd10 = ["I10", "E11", "J45", "C50", "M54", "F32"]  # hypertension, diabetes, asthma, breast cancer, back pain, depression
diagnoses = []
for i in range(1, NUM_DIAGNOSES + 1):
    encid = random.randint(1, NUM_ENCOUNTERS)
    pid = encounters_df.loc[encounters_df.EncounterId == encid, "PatientId"].values[0]
    diagnoses.append([
        i, encid, pid, random.choice(icd10), None, random.choice([0, 1]), random_date(365, 0)
    ])

diagnoses_df = pd.DataFrame(diagnoses, columns=[
    "DiagnosisId", "EncounterId", "PatientId", "ICD10Code", "SNOMEDCode", "IsPrincipal", "DiagnosisDate"
])
diagnoses_df.to_csv(f"{OUTPUT_DIR}/diagnoses.csv", index=False)

# --- Procedures ---
cpt_codes = ["99213", "93000", "70450", "45378", "27447"]
procedures = []
for i in range(1, NUM_PROCEDURES + 1):
    encid = random.randint(1, NUM_ENCOUNTERS)
    pid = encounters_df.loc[encounters_df.EncounterId == encid, "PatientId"].values[0]
    procedures.append([
        i, encid, pid, random.choice(cpt_codes), random_date(365, 0), fake.sentence(nb_words=3)
    ])

procedures_df = pd.DataFrame(procedures, columns=[
    "ProcedureId", "EncounterId", "PatientId", "CPTCode", "ProcedureDate", "ProcedureDescription"
])
procedures_df.to_csv(f"{OUTPUT_DIR}/procedures.csv", index=False)

# --- Labs ---
loinc_codes = ["718-7", "4548-4", "6299-2", "2093-3"]  # Hb, HbA1c, Glucose, Cholesterol
labs = []
for i in range(1, NUM_LABS + 1):
    encid = random.randint(1, NUM_ENCOUNTERS)
    pid = encounters_df.loc[encounters_df.EncounterId == encid, "PatientId"].values[0]
    labs.append([
        i, pid, encid, random.choice(loinc_codes), fake.word(),
        round(random.uniform(3, 15), 2), random.choice(["mg/dL", "g/dL", "mmHg"]),
        random_date(365, 0), "Normal"
    ])

labs_df = pd.DataFrame(labs, columns=[
    "LabResultId", "PatientId", "EncounterId", "LOINCCode", "TestName", "ResultValue",
    "ResultUnit", "ResultDate", "ReferenceRange"
])
labs_df.to_csv(f"{OUTPUT_DIR}/labs.csv", index=False)

# --- Vitals ---
vital_types = ["BP", "HR", "SpO2", "Temp"]
vitals = []
for i in range(1, NUM_VITALS + 1):
    encid = random.randint(1, NUM_ENCOUNTERS)
    pid = encounters_df.loc[encounters_df.EncounterId == encid, "PatientId"].values[0]
    vitals.append([
        i, pid, encid, random.choice(vital_types),
        round(random.uniform(50, 180), 1), random.choice(["mmHg", "bpm", "%", "C"]),
        fake.date_time_this_year()
    ])

vitals_df = pd.DataFrame(vitals, columns=[
    "VitalId", "PatientId", "EncounterId", "ObservationType", "ObservationValue",
    "ObservationUnit", "ObservationDateTime"
])
vitals_df.to_csv(f"{OUTPUT_DIR}/vitals.csv", index=False)

# --- Medications ---
rxnorm = ["1049630", "617314", "198211"]
medications = []
for i in range(1, NUM_MEDICATIONS + 1):
    encid = random.randint(1, NUM_ENCOUNTERS)
    pid = encounters_df.loc[encounters_df.EncounterId == encid, "PatientId"].values[0]
    start = random_date(365, 0)
    end = start + timedelta(days=random.randint(1, 90))
    medications.append([
        i, pid, encid, random.choice(rxnorm), fake.word(),
        f"{random.randint(1, 2)} tablet", random.choice(["Oral", "IV"]),
        start, end, random.randint(1, 30)
    ])

medications_df = pd.DataFrame(medications, columns=[
    "MedicationId", "PatientId", "EncounterId", "RxNormCode", "MedicationName",
    "Dosage", "Route", "StartDate", "EndDate", "DaysSupply"
])
medications_df.to_csv(f"{OUTPUT_DIR}/medications.csv", index=False)

# --- Payers ---
payers = []
for i in range(1, NUM_PAYERS + 1):
    payers.append([
        i, fake.company(), random.choice(["HMO", "PPO", "Medicare", "Medicaid"]),
        random.choice(["East", "West", "North", "South"])
    ])

payers_df = pd.DataFrame(payers, columns=["PayerId", "PayerName", "PlanType", "Region"])
payers_df.to_csv(f"{OUTPUT_DIR}/payers.csv", index=False)

# --- Claims ---
claims = []
for i in range(1, NUM_CLAIMS + 1):
    pid = random.randint(1, NUM_PATIENTS)
    prvid = random.randint(1, NUM_PROVIDERS)
    payid = random.randint(1, NUM_PAYERS)
    sdate = random_date(365, 0)
    claim_amt = round(random.uniform(100, 5000), 2)
    paid_amt = claim_amt if random.random() > 0.2 else round(claim_amt * random.uniform(0.5, 0.9), 2)
    claims.append([
        i, pid, prvid, payid, sdate, claim_amt, paid_amt,
        random.choice(["Submitted", "Adjudicated", "Paid", "Denied"])
    ])

claims_df = pd.DataFrame(claims, columns=[
    "ClaimId", "PatientId", "ProviderId", "PayerId", "ServiceDate",
    "ClaimAmount", "PaidAmount", "ClaimStatus"
])
claims_df.to_csv(f"{OUTPUT_DIR}/claims.csv", index=False)

# --- Devices ---
device_types = ["BP cuff", "Glucose meter", "ECG monitor", "Pulse oximeter"]
devices = []
for i in range(1, NUM_DEVICES + 1):
    devices.append([
        i, random.choice(device_types), fake.company(), fake.uuid4(),
        random.randint(1, NUM_PATIENTS)
    ])

devices_df = pd.DataFrame(devices, columns=["DeviceId", "DeviceType", "Manufacturer", "SerialNumber", "PatientId"])
devices_df.to_csv(f"{OUTPUT_DIR}/devices.csv", index=False)

print(f"✅ Generated synthetic test data in {OUTPUT_DIR}")