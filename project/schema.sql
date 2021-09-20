DROP TABLE IF EXISTS user;

CREATE TABLE user (
    userID TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    telephoneNo TEXT UNIQUE NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE dog (
    dogID TEXT UNIQUE NOT NULL,
    userID TEXT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    breed TEXT NOT NULL,
    lost BIT NOT NULL,


)
