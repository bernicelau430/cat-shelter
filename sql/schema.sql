CREATE TABLE Cat (
    ID VARCHAR(5) PRIMARY KEY,
    Name VARCHAR(255),
    Birthday DATE UNIQUE,
    Gender VARCHAR(10),
    DateArrived DATE,
    Adopted VARCHAR(3) DEFAULT 'No'
);

CREATE TABLE Age (
    Birthday DATE PRIMARY KEY,
    Age INT,
    CatID VARCHAR(5),
    FOREIGN KEY (Birthday) REFERENCES Cat(Birthday),
    FOREIGN KEY (CatID) REFERENCES Cat(ID),
    UNIQUE (Age)
);

CREATE TABLE Age_Range (
    Age INT PRIMARY KEY,
    Age_Range VARCHAR(10),
    AgeID INT UNIQUE,
    FOREIGN KEY (Age) REFERENCES Age(Age),
    FOREIGN KEY (AgeID) REFERENCES Age(Age)
);

CREATE TABLE Applicant (
    ID VARCHAR(5) PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE Adopter (
    ID VARCHAR(5) PRIMARY KEY,
    ApplicantID VARCHAR(5),
    CatID VARCHAR(5),
    FOREIGN KEY (ApplicantID) REFERENCES Applicant(ID),
    FOREIGN KEY (CatID) REFERENCES Cat(ID)
);