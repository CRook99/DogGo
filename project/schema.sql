DROP TABLE IF EXISTS user;

CREATE TABLE user (
    userID INTEGER PRIMARY KEY UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    telephoneNo TEXT UNIQUE NOT NULL,
);

CREATE TABLE dog (
	dogID INTEGER PRIMARY KEY NOT NULL UNIQUE,
	userID INTEGER NOT NULL,
	name TEXT NOT NULL CHECK(length(name) >= 1 AND length(name) <= 20),
	age	INTEGER NOT NULL CHECK(age >= 0 AND age <= 20),
	sex	TEXT NOT NULL CHECK(sex == "M" OR sex == "F"),
	breed TEXT NOT NULL CHECK(length(breed) >= 1 AND length(breed) <= 50),
	lost BOOLEAN NOT NULL CHECK(lost == 0 OR lost == 1),
	last_report	TEXT NOT NULL,
	location TEXT NOT NULL,
	FOREIGN KEY(userID) REFERENCES user(userID)
);

INSERT INTO dog VALUES