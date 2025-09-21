# 📂 Input Files for Fabric Patient Data Demo

This demo project uses a set of **synthetic CSV files** that represent healthcare data feeds from EHR, labs, pharmacy, devices, and payers. These files land in the **Bronze layer** of OneLake and serve as input for transformations and standardization.

---

### 1. patients.csv
- **Source**: EHR/EMR system export.  
- **Purpose**: Holds patient demographics and identifiers.  
- **Key Fields**:  
  - PatientId (local MRN from source)  
  - FirstName, LastName  
  - DOB (date of birth)  
  - Gender  
  - Phone, Email  
  - AddressLine1, City, State, PostalCode  
  - SourceSystem (Epic, Cerner, etc.)  

### 2. providers.csv
- **Source**: Provider directory / HR system.  
- **Purpose**: Defines healthcare practitioners.  
- **Key Fields**:  
  - ProviderId  
  - FirstName, LastName  
  - NPI (National Provider Identifier)  
  - Specialty  
  - Organization  
  - LocationId  

### 3. locations.csv
- **Source**: Hospital/clinic master data.  
- **Purpose**: Defines where encounters occur.  
- **Key Fields**:  
  - LocationId  
  - LocationName (Hospital, Clinic, Lab)  
  - AddressLine1, City, State, PostalCode  
  - Region  

### 4. encounters.csv
- **Source**: EHR visit logs.  
- **Purpose**: Captures patient visits (admissions, appointments).  
- **Key Fields**:  
  - EncounterId  
  - PatientId (FK → patients.csv)  
  - ProviderId (FK → providers.csv)  
  - LocationId (FK → locations.csv)  
  - EncounterDate  
  - EncounterType (Inpatient, Outpatient, ER, Telehealth)  
  - DischargeDate  
  - LengthOfStay  

### 5. diagnoses.csv
- **Source**: EHR problem list or coding system.  
- **Purpose**: Clinical diagnoses per encounter.  
- **Key Fields**:  
  - DiagnosisId  
  - EncounterId (FK → encounters.csv)  
  - PatientId (FK → patients.csv)  
  - ICD10Code  
  - SNOMEDCode (optional)  
  - IsPrincipal (flag for primary diagnosis)  
  - DiagnosisDate  

### 6. procedures.csv
- **Source**: EHR / billing feeds.  
- **Purpose**: Captures medical procedures performed.  
- **Key Fields**:  
  - ProcedureId  
  - EncounterId  
  - PatientId  
  - CPTCode (or HCPCS)  
  - ProcedureDate  
  - ProcedureDescription  

### 7. labs.csv
- **Source**: LIS (Laboratory Information System).  
- **Purpose**: Stores lab test results.  
- **Key Fields**:  
  - LabResultId  
  - PatientId  
  - EncounterId  
  - LOINCCode  
  - TestName  
  - ResultValue  
  - ResultUnit  
  - ResultDate  
  - ReferenceRange  

### 8. vitals.csv
- **Source**: Bedside devices / IoT / nursing notes.  
- **Purpose**: Captures vital signs at encounter.  
- **Key Fields**:  
  - VitalId  
  - PatientId  
  - EncounterId  
  - ObservationType (BP, HR, SpO₂, Temp)  
  - ObservationValue  
  - ObservationUnit  
  - ObservationDateTime  

### 9. medications.csv
- **Source**: Pharmacy system / EHR orders.  
- **Purpose**: Captures prescribed/administered drugs.  
- **Key Fields**:  
  - MedicationId  
  - PatientId  
  - EncounterId  
  - RxNormCode  
  - MedicationName  
  - Dosage  
  - Route (oral, IV, etc.)  
  - StartDate, EndDate  
  - DaysSupply  

### 10. claims.csv
- **Source**: Payer/billing system.  
- **Purpose**: Financial claim submissions & adjudications.  
- **Key Fields**:  
  - ClaimId  
  - PatientId  
  - ProviderId  
  - PayerId  
  - ServiceDate  
  - ClaimAmount  
  - PaidAmount  
  - ClaimStatus (Submitted, Adjudicated, Paid, Denied)  

### 11. payers.csv
- **Source**: Insurance companies / payers.  
- **Purpose**: Defines payer master data.  
- **Key Fields**:  
  - PayerId  
  - PayerName  
  - PlanType (HMO, PPO, Medicare, Medicaid)  
  - Region  

### 12. devices.csv (optional — IoT streaming demo)
- **Source**: Device registry.  
- **Purpose**: Describes devices generating vital/observation data.  
- **Key Fields**:  
  - DeviceId  
  - DeviceType (BP cuff, Glucose meter, etc.)  
  - Manufacturer  
  - SerialNumber  
  - PatientId (if assigned)  

---

✅ With these **12 input files**, the demo can simulate data ingestion from **EHR, labs, vitals, pharmacy, devices, and payers**, which will then be standardized and modeled into the Gold schema in Fabric.
