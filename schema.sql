CREATE DATABASE IF NOT EXISTS pompa;
USE pompa;

CREATE TABLE Hospital (
    hospital_id INT,
    name VARCHAR(40),
    city VARCHAR(40),
    PRIMARY KEY (hospital_id)
);

CREATE TABLE User (
    TCK INT,
    password VARCHAR(40),
    fullname VARCHAR(255),
    address VARCHAR(255),
    birth_year INT,
    role VARCHAR(40),
    PRIMARY KEY (TCK)
);

CREATE TABLE Admin (
    admin_id INT,
    PRIMARY KEY (admin_id)
);

CREATE TABLE Doctor (
    TCK INT,
    expertise_field VARCHAR(40),
    hospital_id INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (hospital_id) REFERENCES Hospital(hospital_id),
    FOREIGN KEY (TCK) REFERENCES User(TCK)
);

CREATE TABLE BankAccount (
    bank_account_no INT,
    bank_account_password VARCHAR(40),
    active VARCHAR(40),
    balance INT,
    PRIMARY KEY (bank_account_no)
);

CREATE TABLE Patient (
    TCK INT,
    bank_account_no INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (bank_account_no) REFERENCES BankAccount(bank_account_no),
    FOREIGN KEY (TCK) REFERENCES User(TCK)
);

CREATE TABLE Prescription (
    presc_id INT,
    date DATETIME,
    PRIMARY KEY (presc_id)
);

CREATE TABLE Prescribes (
    doctor_TCK INT,
    patient_TCK INT,
    presc_id INT,
    PRIMARY KEY (doctor_TCK, patient_TCK, presc_id),
    FOREIGN KEY (doctor_TCK) REFERENCES User(TCK),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (presc_id) REFERENCES Prescription(presc_id)
);

CREATE TABLE Illness (
    illness_name VARCHAR(40),
    type VARCHAR(40),
    PRIMARY KEY (illness_name)
);

CREATE TABLE HasIllness (
    patient_TCK INT,
    illness_name VARCHAR(40),
    PRIMARY KEY (patient_TCK, illness_name),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (illness_name) REFERENCES Illness(illness_name)
);

CREATE TABLE PharmaceuticalWarehouse (
    warehouse_id INT NOT NULL,
    warehouse_name VARCHAR(40),
    warehouse_city VARCHAR(40),
    PRIMARY KEY (warehouse_id)
);

CREATE TABLE PharmaceuticalWarehouseWorker (
    TCK INT NOT NULL,
    warehouse_id INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (TCK) REFERENCES User(TCK),
    FOREIGN KEY (warehouse_id) REFERENCES PharmaceuticalWarehouse(warehouse_id)
);

CREATE TABLE Pharmacy (
    pharmacy_id INT NOT NULL,
    pharm_name VARCHAR(255),
    pharm_city VARCHAR(40),
    PRIMARY KEY (pharmacy_id)
);

CREATE TABLE Pharmacist (
    TCK INT NOT NULL,
    pharmacy_id INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (TCK) REFERENCES User(TCK),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(pharmacy_id)
);

CREATE TABLE Drug (
    name VARCHAR(255) NOT NULL,
    needs_prescription VARCHAR(255),
    drug_class VARCHAR(255),
    drug_type VARCHAR(255),
    price INT,
    PRIMARY KEY (name)
);

CREATE TABLE Restocks (
    pharm_id INT,
    warehouse_id INT,
    drug_name VARCHAR(255),
    restock_count INT,
    restock_date DATETIME,
    PRIMARY KEY (pharm_id, warehouse_id, drug_name),
    FOREIGN KEY (pharm_id) REFERENCES Pharmacy(pharmacy_id),
    FOREIGN KEY (warehouse_id) REFERENCES PharmaceuticalWarehouse(warehouse_id),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

CREATE TABLE HasDrug (
    drug_name VARCHAR(255) NOT NULL,
    pharmacy_id INT NOT NULL,
    drug_count INT NOT NULL,
    PRIMARY KEY (drug_name, pharmacy_id),
    FOREIGN KEY (drug_name) REFERENCES Drug(name),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(pharmacy_id)
);

CREATE TABLE SideEffect (
    effect_name VARCHAR(255) NOT NULL,
    drug_name VARCHAR(255) NOT NULL,
    intensity INT,
    PRIMARY KEY (effect_name),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

CREATE TABLE Dosage (
    age_group VARCHAR(255) NOT NULL,
    no_per_day INT NOT NULL,
    dosage_per_use INT NOT NULL,
    PRIMARY KEY (age_group, no_per_day, dosage_per_use)
);

CREATE TABLE Orders (
    bank_account_no INT,
    patient_TCK INT,
    drug_name VARCHAR(255),
    order_date DATETIME,
    count INT,
    status VARCHAR(40),
    PRIMARY KEY (bank_account_no, drug_name, patient_TCK),
    FOREIGN KEY (bank_account_no) REFERENCES BankAccount(bank_account_no),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

CREATE TABLE Contains (
    presc_id INT,
    drug_name VARCHAR(255),
    PRIMARY KEY (presc_id, drug_name),
    FOREIGN KEY (presc_id) REFERENCES Prescription(presc_id),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

CREATE TABLE HasBankAccount (
    bank_account_no INT,
    patient_TCK INT,
    PRIMARY KEY (bank_account_no, patient_TCK),
    FOREIGN KEY (bank_account_no) REFERENCES BankAccount(bank_account_no),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK)
);

CREATE TABLE HasDosage (
    drug_name varchar(255) NOT NULL,
    age_group VARCHAR(255) NOT NULL,
    no_per_day INT NOT NULL,
    dosage_per_use INT NOT NULL,
    PRIMARY KEY (drug_name, age_group, no_per_day, dosage_per_use),
    FOREIGN KEY (age_group, no_per_day, dosage_per_use) REFERENCES Dosage(age_group, no_per_day, dosage_per_use),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

INSERT INTO Drug(name, needs_prescription, drug_class, drug_type, price)
VALUES("teraflu", "no", "flu drug", "drug type", 56);

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212121, 'şifre', 'Big Dick', 'Bilkent üniversitesi çankaya/ankara', 2001, 'doctor');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212122, 'şifre', 'Big Patient', 'maltepe üniversitesi çankaya/ankara', 2002, 'patient');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212123, 'şifre', 'benim adim eczaci', 'eczaci adres', 1985, 'pharmacist');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212124, 'şifre', 'benim isim Pharmaceutical Warehouse', 'işçi adresi', 1903, 'pharmaceuticalwarehouseworker');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212125, 'şifre admin', 'benim isim admin', 'admin adresi', 1905, 'admin');

INSERT INTO Admin(admin_id)
VALUES(1);

INSERT INTO Hospital(hospital_id, name, city)
VALUES(1, 'Başibüyük Hastanesi', 'Adana');

INSERT INTO Doctor(TCK, expertise_field, hospital_id)
VALUES(2121212121, 'üroloji', 1);

INSERT INTO BankAccount(bank_account_no, bank_account_password, active, balance)
VALUES(3131, 'banka şifre', 'aktif', 1000);

INSERT INTO Patient(TCK, bank_account_no)
VALUES(2121212122, 3131);

INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city)
VALUES(1, 'Faruk Eczanesi', 'pompa city');

INSERT INTO Pharmacist(TCK, pharmacy_id)
VALUES(2121212123, 1);

INSERT INTO PharmaceuticalWarehouse(warehouse_id, warehouse_name, warehouse_city)
VALUES(1, 'Bizim Depo', 'Ankara');

INSERT INTO PharmaceuticalWarehouseWorker(TCK, warehouse_id)
VALUES(2121212124, 1);

INSERT INTO Illness(illness_name, type)
VALUES('Flu', 'öldürücü değil');

INSERT INTO HasIllness(patient_TCK, illness_name)
VALUES(2121212122, 'Flu');

INSERT INTO Prescription(presc_id, date)
VALUES(1, '2023-03-14 09:00:00');
