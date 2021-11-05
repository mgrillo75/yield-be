create table articles(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(100),
  body INTEGER(255),
  deposit INTEGER(255),
  date datetime default current_timestamp
);