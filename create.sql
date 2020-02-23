CREATE TABLE WEIGHT(
    timestamp INTEGER PRIMARY KEY,
    datetime TEXT NOT NULL,
    weight REAL NOT NULL,
    loss REAL NOT NULL,
    CHECK (timestamp > 1577836800 AND
           weight > 0)
);
