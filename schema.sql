CREATE DATABASE IF NOT EXISTS pompa;
USE pompa;

CREATE TABLE Hospital (
    hospital_id INT,
    name VARCHAR(40),
    city VARCHAR(40),
    PRIMARY KEY (hospital_id)
);

CREATE TABLE User (
    TCK BIGINT,
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
    TCK BIGINT,
    expertise_field VARCHAR(40),
    hospital_id INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (hospital_id) REFERENCES Hospital(hospital_id),
    FOREIGN KEY (TCK) REFERENCES User(TCK)
);

CREATE TABLE Patient (
    TCK BIGINT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (TCK) REFERENCES User(TCK)
);

CREATE TABLE BankAccount (
    bank_account_no INT,
    bank_account_password VARCHAR(40),
    active VARCHAR(40),
    balance INT,
    patient_TCK BIGINT,
    PRIMARY KEY (bank_account_no),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK)
);

CREATE TABLE Prescription (
    presc_id INT NOT NULL AUTO_INCREMENT,
    date DATETIME,
    PRIMARY KEY (presc_id)
);

CREATE TABLE Prescribes (
    doctor_TCK BIGINT,
    patient_TCK BIGINT,
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
    patient_TCK BIGINT,
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
    TCK BIGINT NOT NULL,
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
    TCK BIGINT NOT NULL,
    pharmacy_id INT,
    PRIMARY KEY (TCK),
    FOREIGN KEY (TCK) REFERENCES User(TCK),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacy(pharmacy_id)
);

CREATE TABLE Drug (
    name VARCHAR(255) NOT NULL,
    needs_prescription VARCHAR(255),
    company VARCHAR(255),
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
    PRIMARY KEY (effect_name),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

-- CREATE TABLE Dosage (
--     age_group VARCHAR(255) NOT NULL,
--     no_per_day INT NOT NULL,
--     dosage_per_use INT NOT NULL,
--     PRIMARY KEY (age_group, no_per_day, dosage_per_use)
-- );

CREATE TABLE Orders (
    bank_account_no INT,
    patient_TCK BIGINT,
    drug_name VARCHAR(255),
    order_date DATETIME,
    count INT,
    status VARCHAR(40),
    PRIMARY KEY (bank_account_no, drug_name, patient_TCK, order_date),
    FOREIGN KEY (bank_account_no) REFERENCES BankAccount(bank_account_no),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);
CREATE TABLE Cart (
    TCK BIGINT,
    drug_name VARCHAR(255),
    drug_count INT,
    pharm_id INT,
    PRIMARY KEY (TCK, drug_name, pharm_id),
    FOREIGN KEY (TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);

CREATE TABLE Contains (
    presc_id INT,
    drug_name VARCHAR(255),
    PRIMARY KEY (presc_id, drug_name),
    FOREIGN KEY (presc_id) REFERENCES Prescription(presc_id),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);


-- CREATE TABLE HasDosage (
--     drug_name varchar(255) NOT NULL,
--     age_group VARCHAR(255) NOT NULL,
--     no_per_day INT NOT NULL,
--     dosage_per_use INT NOT NULL,
--     PRIMARY KEY (drug_name, age_group, no_per_day, dosage_per_use),
--     FOREIGN KEY (age_group, no_per_day, dosage_per_use) REFERENCES Dosage(age_group, no_per_day, dosage_per_use),
--     FOREIGN KEY (drug_name) REFERENCES Drug(name)
-- );
CREATE VIEW CartView AS
SELECT drug_name, drug_count, TCK, drug_count * price AS total_price
FROM Cart JOIN Drug  ON drug_name = name ;

-- CREATE VIEW PastOrderView AS
-- SELECT *
-- FROM Orders o, Orders p
-- WHERE o.patient_TCK = p.patient_TCK AND o.bank_account_no = p.bank_account_no AND o.order_date = p.order_date AND o.drug_name <> p.drug_name;

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("teraflu", "no", "abc", "drug type", 56);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("aferin", "no", "abc", "drug type", 15);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("nurofen", "no", "pompake", "drug type", 20);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("arveles", "no", "amciksirketi", "drug type", 25);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("xanax", "yes", "psikolojik sirketi", "drug type", 100);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("paxera", "yes", "depression sirketi", "drug type", 90);

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212121, 'passwordDoctor', 'Big Dick', 'Bilkent university cankaya/ankara', 2001, 'doctor');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212122, 'passwordPatient', 'Big Patient', 'maltepe university cankaya/ankara', 2002, 'patient');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212123, 'passwordPharmacist', 'benim adim eczaci', 'eczaci adres', 1985, 'pharmacist');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212124, 'passwordWorker', 'benim isim Pharmaceutical Warehouse', 'worker adresi', 1903, 'pharmaceuticalwarehouseworker');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2121212125, 'password admin', 'benim isim admin', 'admin adresi', 1905, 'admin');

INSERT INTO Admin(admin_id)
VALUES(1);

INSERT INTO Hospital(hospital_id, name, city)
VALUES(1, 'Basibuyuk Hastanesi', 'Adana');

INSERT INTO Doctor(TCK, expertise_field, hospital_id)
VALUES(2121212121, 'dick science', 1);

INSERT INTO Patient(TCK)
VALUES(2121212122);

INSERT INTO BankAccount(bank_account_no, bank_account_password, active, balance, patient_TCK)
VALUES(3131, 'banka password', 'active', 1000, 2121212122);

INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city)
VALUES(1, 'Faruk Eczanesi', 'pompa city');

INSERT INTO Pharmacist(TCK, pharmacy_id)
VALUES(2121212123, 1);

INSERT INTO PharmaceuticalWarehouse(warehouse_id, warehouse_name, warehouse_city)
VALUES(1, 'Bizim Depo', 'Ankara');

INSERT INTO PharmaceuticalWarehouseWorker(TCK, warehouse_id)
VALUES(2121212124, 1);

INSERT INTO Illness(illness_name, type)
VALUES('Flu', 'not killing');

INSERT INTO HasIllness(patient_TCK, illness_name)
VALUES(2121212122, 'Flu');

INSERT INTO Prescription( date)
VALUES( '2023-03-14 09:00:00');

INSERT INTO Contains(presc_id, drug_name)
VALUES(1, "paxera");

INSERT INTO Prescribes(presc_id, doctor_TCK, patient_TCK)
VALUES(1, 2121212121, 2121212122);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("teraflu", 1, 10);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("aferin", 1, 12);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("paxera", 1, 5);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("arveles", 1, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("nurofen", 1, 5);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("xanax", 1, 5);

INSERT INTO Cart(TCK, drug_name, drug_count, pharm_id )
VALUES( 2121212122, "teraflu", 3,1 );
