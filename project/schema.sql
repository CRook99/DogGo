DROP TABLE IF EXISTS user;

CREATE TABLE user (
    userID INTEGER PRIMARY KEY UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    telephoneNo TEXT UNIQUE NOT NULL,
);

CREATE TABLE dog (
	dogID INTEGER PRIMARY KEY UNIQUE NOT NULL,
	userID INTEGER NOT NULL,
	name TEXT NOT NULL CHECK (length(name) IN (1, 20)),
	age INTEGER NOT NULL CHECK (age IN (0, 20)),
	sex TEXT NOT NULL CHECK (sex == "M" OR sex == "F"),
	breed TEXT NOT NULL CHECK (length(breed) IN (1, 50)),
	lost BOOLEAN NOT NULL CHECK (lost IN (0, 1)),
	last_report TEXT NOT NULL,
	location TEXT NOT NULL,
	FOREIGN KEY(userID) REFERENCES user(userID)
);