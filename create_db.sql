DROP TABLE IF EXISTS frequencies;

CREATE TABLE frequencies (
  letter1   INT  NOT NULL,
  letter2   INT  NOT NULL,
  letter3   INT  NOT NULL,
  letter4   INT  NOT NULL,
  letter5   INT  NOT NULL,
  frequency REAL NOT NULL,
  PRIMARY KEY (letter1, letter2, letter3, letter4, letter5)
);
