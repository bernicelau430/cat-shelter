-- Insert sample data into Cat table
INSERT INTO Cat (ID, Name, Birthday, Gender, DateArrived, Adopted) VALUES
('A9834', 'Whiskers', '2021-05-01', 'Male', '2021-06-01', 'No'),
('B2341', 'Mittens', '2020-08-15', 'Female', '2020-09-01', 'No'),
('C9384', 'Shadow', '2019-11-20', 'Male', '2019-12-01', 'Yes');

-- Insert sample data into Age table with calculated age
INSERT INTO Age (Birthday, Age, CatID) VALUES
('2021-05-01', FLOOR(DATEDIFF(CURDATE(), '2021-05-01') / 365), 'A9834'),
('2020-08-15', FLOOR(DATEDIFF(CURDATE(), '2020-08-15') / 365), 'B2341'),
('2019-11-20', FLOOR(DATEDIFF(CURDATE(), '2019-11-20') / 365), 'C9384');

-- Insert sample data into Age_Range table
INSERT INTO Age_Range (Age, Age_Range, AgeID) VALUES
(2, 'Young', 1),
(3, 'Adult', 2),
(4, 'Adult', 3);

-- Insert sample data into Applicant table
INSERT INTO Applicant (ID, Name, Email) VALUES
('D8391', 'John Doe', 'john.doe@example.com'),
('E3255', 'Jane Smith', 'jane.smith@example.com');

-- Insert sample data into Adopter table
INSERT INTO Adopter (ID, ApplicantID, CatID) VALUES
('F6774', 'D8391', 'C9384');