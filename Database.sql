CREATE DATABASE trainingmanagement;

CREATE TABLE Account
(
	accID varchar(15) NOT NULL,
	accType varchar(8),
	accName varchar(50),
	accPassword varchar(20),
	accEmail varchar(50) CHECK(accEmail LIKE '%_@_%_.__%'),
	PRIMARY KEY(accID)
);

CREATE TABLE Administrator
(
	accID varchar(15) NOT NULL,
	adminID varchar(15) NOT NULL,
	adminName varchar(50),
	PRIMARY KEY(accID, adminID),
	FOREIGN KEY(accID) REFERENCES Account(accID)
);

CREATE TABLE Trainer
(
	accID varchar(15) NOT NULL,
	trainerID varchar(15) NOT NULL,
	trainerName varchar(50),
	PRIMARY KEY(accID, trainerID),
	FOREIGN KEY(accID) REFERENCES Account(accID)
);

CREATE TABLE Trainee
(
	accID varchar(15) NOT NULL,
	traineeID varchar(15) NOT NULL,
	traineeName varchar(50),
	PRIMARY KEY(accID, traineeID),
	FOREIGN KEY(accID) REFERENCES Account(accID)
);

ALTER TABLE Trainer ADD CONSTRAINT trainerID_unq unique(trainerID);

CREATE TABLE Course
(
	trainerID varchar(15) NOT NULL,
	courseID varchar(5) NOT NULL,
	courseName varchar(50),
	PRIMARY KEY(trainerID, courseID),
	FOREIGN KEY(trainerID) REFERENCES Trainer(trainerID)
);

ALTER TABLE Course ADD CONSTRAINT courseID_unq unique(courseID);

CREATE TABLE Training_Materials
(
	courseName varchar(50) NOT NULL,
	materialID varchar(6) NOT NULL,
	materialName varchar(50),
    materialContent varchar(5000),
	PRIMARY KEY(courseName, materialID)
);

ALTER TABLE Trainee ADD CONSTRAINT traineeID_unq unique(traineeID);

CREATE TABLE Feedback
(
	traineeID varchar(15) NOT NULL,
    courseName varchar(50) NOT NULL,
	feedbackID varchar(6) NOT NULL,
	feedbackTitle varchar(50),
	feedbackContent varchar(500),
	PRIMARY KEY(traineeID, courseName, feedbackID),
    FOREIGN KEY(traineeID) REFERENCES Trainee(traineeID)
);
