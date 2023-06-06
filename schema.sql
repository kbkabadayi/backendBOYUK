CREATE DATABASE IF NOT EXISTS pharmhub;
USE pharmhub;

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
    illness VARCHAR(255),
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

CREATE TABLE Orders (
    bank_account_no INT,
    patient_TCK BIGINT,
    drug_name VARCHAR(255),
    order_date DATETIME,
    count INT,
    total_price INT,
    PRIMARY KEY (bank_account_no, drug_name, patient_TCK, order_date),
    FOREIGN KEY (bank_account_no) REFERENCES BankAccount(bank_account_no),
    FOREIGN KEY (patient_TCK) REFERENCES Patient(TCK),
    FOREIGN KEY (drug_name) REFERENCES Drug(name)
);
CREATE TABLE Cart (
    TCK BIGINT,
    drug_name VARCHAR(255),
    drug_count INT,
    PRIMARY KEY (TCK, drug_name),
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

CREATE VIEW CartView AS
SELECT drug_name, company, needs_prescription, drug_count, TCK, price
FROM Cart JOIN Drug  ON drug_name = name ;

CREATE VIEW RestockView AS
SELECT pharm_name, drug_name, restock_count, restock_date, warehouse_id
FROM Restocks JOIN Pharmacy ON pharm_id = pharmacy_id;

CREATE VIEW OrdersView AS
SELECT O.bank_account_no, O.patient_TCK, O.drug_name, O.order_date, O.count, D.price * O.count AS total_price
FROM Orders O
JOIN Drug D ON O.drug_name = D.name;

DELIMITER //

CREATE TRIGGER DrugInsertTrigger
AFTER INSERT ON Drug
FOR EACH ROW
BEGIN
    IF NEW.name NOT IN (SELECT drug_name FROM HasDrug) THEN
        INSERT INTO HasDrug (drug_name, pharmacy_id, drug_count)
        SELECT NEW.name, pharmacy_id, 0
        FROM (SELECT DISTINCT pharmacy_id FROM HasDrug) AS pharmacy_ids;
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER PharmacyInsertTrigger
AFTER INSERT ON Pharmacy
FOR EACH ROW
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_drug_names (name VARCHAR(255));
    
    INSERT INTO tmp_drug_names (name)
    SELECT name FROM Drug;
    
    INSERT INTO HasDrug (drug_name, pharmacy_id, drug_count)
    SELECT name, NEW.pharmacy_id, 0
    FROM tmp_drug_names;
    
    DROP TEMPORARY TABLE IF EXISTS tmp_drug_names;
END //

DELIMITER ;

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Theraflu", "no", "GSK", "Flu", 56);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Aferin", "no", "Forte", "Flu", 15);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Nurofen", "no", "Benckiser's", "Pain Killer", 20);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Arveles", "no", "Pfizer", "Pain Killer", 25);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Xanax", "yes", "Abdi Ibrahim", "Anti Depressant", 100);

INSERT INTO Drug(name, needs_prescription, company, drug_type, price)
VALUES("Paxera", "yes", "Abdi Ibrahim", "Anti Depressant", 90);

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(1, '1', 'Boran Torun', 'Bilkent University Cankaya/Ankara', 2001, 'doctor');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(2, '2', 'Kaan Berk Kabadayi', 'Bilkent Universitesi, 82. yurt', 2002, 'patient');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(3, '3', 'Ozgur Ulusoy', 'Bilkent Universitesi, EA Binasi', 2002, 'patient');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(4, '4', 'Yarkin Sakinci', 'Bilkent Universitesi, 82. yurt', 2002, 'patient');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(11, '11', 'Mehmet Onur Uysal', 'Universiteler Mahallesi, No: 26, Cankaya/Ankara', 1985, 'pharmacist');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(31, '31', 'Ugur Can Altun', 'worker adresi', 1903, 'pharmaceuticalwarehouseworker');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(0, '0', 'admin', 'admin', 1905, 'admin');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(12, '12', 'Ahmet Onur Uysal', 'Universiteler Mahallesi, No: 26, Cankaya/Ankara', 1985, 'pharmacist');

INSERT INTO User(TCK, password, fullname, address, birth_year, role)
VALUES(5, '5', 'Ahmet Torun', 'Bilkent University Cankaya/Ankara', 2001, 'doctor');

INSERT INTO Admin(admin_id)
VALUES(0);

INSERT INTO Hospital(hospital_id, name, city)
VALUES(1, 'Bilkent Sehir Hastanesi', 'Ankara');

INSERT INTO Doctor(TCK, expertise_field, hospital_id)
VALUES(1, 'Urology', 1);

INSERT INTO Doctor(TCK, expertise_field, hospital_id)
VALUES(5, 'Gastroentrology', 1);

INSERT INTO Patient(TCK)
VALUES(2);

INSERT INTO Patient(TCK)
VALUES(3);

INSERT INTO Patient(TCK)
VALUES(4);

INSERT INTO BankAccount(bank_account_no, bank_account_password, active, balance, patient_TCK)
VALUES(1, 'banka password', 'active', 1000, 2);

INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city)
VALUES(1, 'Faruk Eczanesi', 'Ankara');

INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city)
VALUES(2, 'Gultekin Eczanesi', 'Ankara');

INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city)
VALUES(3, 'Uysal Eczanesi', 'Ankara');

INSERT INTO Pharmacist(TCK, pharmacy_id)
VALUES(11, 1);

INSERT INTO Pharmacist(TCK, pharmacy_id)
VALUES(12, 2);

INSERT INTO PharmaceuticalWarehouse(warehouse_id, warehouse_name, warehouse_city)
VALUES(1, 'Bizim Depo', 'Ankara');

INSERT INTO PharmaceuticalWarehouseWorker(TCK, warehouse_id)
VALUES(31, 1);

INSERT INTO Prescription( date, illness)
VALUES( '2023-03-14 09:00:00', "Covid-19");

INSERT INTO Contains(presc_id, drug_name)
VALUES(1, "Paxera");

INSERT INTO Prescribes(presc_id, doctor_TCK, patient_TCK)
VALUES(1, 1, 2);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Theraflu", 1, 20);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Aferin", 1, 20);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Paxera", 1, 20);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Arveles", 1, 20);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Nurofen", 1, 20);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Xanax", 1, 20);

--
INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Theraflu", 2, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Aferin", 2, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Paxera", 2, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Arveles", 2, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Nurofen", 2, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Xanax", 2, 0);

--

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Theraflu", 3, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Aferin", 3, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Paxera", 3, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Arveles", 3, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Nurofen", 3, 0);

INSERT INTO HasDrug(drug_name, pharmacy_id, drug_count)
VALUES("Xanax", 3, 0);

INSERT INTO Restocks( pharm_id, warehouse_id , drug_name, restock_count, restock_date)
VALUES (1, 1, "Paxera", 25, '2023-01-01 14:15:00');
