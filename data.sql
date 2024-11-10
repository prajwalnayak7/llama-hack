-- Create the patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    mrn VARCHAR(10) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    admission_date TIMESTAMP,
    discharge_date TIMESTAMP,
    primary_diagnosis VARCHAR(100),
    insurance_provider VARCHAR(50),
    room_number VARCHAR(10)
);

-- Insert 100 sample patients
INSERT INTO patients (mrn, first_name, last_name, date_of_birth, gender, blood_type, admission_date, discharge_date, primary_diagnosis, insurance_provider, room_number)
SELECT 
    'MRN' || LPAD(CAST(generate_series AS VARCHAR), 6, '0') as mrn,
    CASE (random() * 19)::INTEGER
        WHEN 0 THEN 'James' WHEN 1 THEN 'John' WHEN 2 THEN 'Robert' 
        WHEN 3 THEN 'Mary' WHEN 4 THEN 'Patricia' WHEN 5 THEN 'Jennifer'
        WHEN 6 THEN 'Michael' WHEN 7 THEN 'William' WHEN 8 THEN 'David'
        WHEN 9 THEN 'Linda' WHEN 10 THEN 'Elizabeth' WHEN 11 THEN 'Sarah'
        WHEN 12 THEN 'Richard' WHEN 13 THEN 'Joseph' WHEN 14 THEN 'Thomas'
        WHEN 15 THEN 'Barbara' WHEN 16 THEN 'Susan' WHEN 17 THEN 'Jessica'
        WHEN 18 THEN 'Charles' WHEN 19 THEN 'Karen'
    END as first_name,
    CASE (random() * 19)::INTEGER
        WHEN 0 THEN 'Smith' WHEN 1 THEN 'Johnson' WHEN 2 THEN 'Williams'
        WHEN 3 THEN 'Brown' WHEN 4 THEN 'Jones' WHEN 5 THEN 'Garcia'
        WHEN 6 THEN 'Miller' WHEN 7 THEN 'Davis' WHEN 8 THEN 'Rodriguez'
        WHEN 9 THEN 'Martinez' WHEN 10 THEN 'Anderson' WHEN 11 THEN 'Taylor'
        WHEN 12 THEN 'Thomas' WHEN 13 THEN 'Moore' WHEN 14 THEN 'Jackson'
        WHEN 15 THEN 'Martin' WHEN 16 THEN 'Lee' WHEN 17 THEN 'Thompson'
        WHEN 18 THEN 'White' WHEN 19 THEN 'Harris'
    END as last_name,
    (CURRENT_DATE - (random() * 365 * 80)::INTEGER * INTERVAL '1 day')::DATE as date_of_birth,
    CASE WHEN random() < 0.5 THEN 'Male' ELSE 'Female' END as gender,
    (ARRAY['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])[floor(random() * 8 + 1)] as blood_type,
    CURRENT_TIMESTAMP - (random() * 30)::INTEGER * INTERVAL '1 day' as admission_date,
    CASE 
        WHEN random() < 0.7 
        THEN CURRENT_TIMESTAMP + (random() * 10)::INTEGER * INTERVAL '1 day'
        ELSE NULL 
    END as discharge_date,
    CASE (random() * 9)::INTEGER
        WHEN 0 THEN 'Pneumonia'
        WHEN 1 THEN 'Fractured Femur'
        WHEN 2 THEN 'Acute Appendicitis'
        WHEN 3 THEN 'Myocardial Infarction'
        WHEN 4 THEN 'Type 2 Diabetes'
        WHEN 5 THEN 'Chronic Kidney Disease'
        WHEN 6 THEN 'Asthma Exacerbation'
        WHEN 7 THEN 'COVID-19'
        WHEN 8 THEN 'Hypertensive Crisis'
        WHEN 9 THEN 'Gastroenteritis'
    END as primary_diagnosis,
    CASE (random() * 7)::INTEGER
        WHEN 0 THEN 'Blue Cross'
        WHEN 1 THEN 'Aetna'
        WHEN 2 THEN 'UnitedHealth'
        WHEN 3 THEN 'Cigna'
        WHEN 4 THEN 'Medicare'
        WHEN 5 THEN 'Medicaid'
        WHEN 6 THEN 'Kaiser Permanente'
        WHEN 7 THEN 'Humana'
    END as insurance_provider,
    CONCAT(
        floor(random() * 5 + 1),
        floor(random() * 100 + 1)::TEXT
    ) as room_number
FROM generate_series(1, 100);

-- Create index on MRN for faster lookups
CREATE INDEX idx_patient_mrn ON patients(mrn);