import sqlite3

conn = sqlite3.connect("fin_bd.s3db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cursor.executescript("""
PRAGMA foreign_keys = on;
""")

cursor.executescript("""
DROP TABLE IF EXISTS students;
CREATE TABLE students (
  student_id SMALLINT NOT NULL PRIMARY KEY,
  last_name VARCHAR(15),
  first_name VARCHAR(15),
  status VARCHAR(15),
  group_number SMALLINT,
  stream_id SMALLINT NOT NULL,
  FOREIGN KEY (stream_id) REFERENCES streams(stream_id)
  );  
""")

cursor.executescript("""
DROP TABLE IF EXISTS streams;
CREATE TABLE streams (
  stream_id SMALLINT NOT NULL PRIMARY KEY,
  faculty VARCHAR(15),
  student_amount SMALLINT,
  receipt_year SMALLINT
  );
""")

cursor.executescript("""
INSERT INTO streams VALUES (1, 'FRTK', 143, 2017);
""")

cursor.executescript("""
INSERT INTO students VALUES (1, 'Ivan', 'Markin', 'In University', 719, 1);
""")

cursor.executescript("""
DROP TABLE IF EXISTS exams;
CREATE TABLE exams (
  exam_id SMALLINT NOT NULL PRIMARY KEY,
  exam_name VARCHAR(15),
  exam_date DATE,
  department_id SMALLINT NOT NULL,
  grading_system VARCHAR(15),
  session_id SMALLINT NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
  FOREIGN KEY (session_id) REFERENCES sessions(session_id)
  );
""")

cursor.executescript("""
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
  department_id SMALLINT NOT NULL PRIMARY KEY,
  department_name VARCHAR(15),
  professors_amount SMALLINT,
  hours_number SMALLINT
  );
""")

cursor.executescript("""
DROP TABLE IF EXISTS sessions;
CREATE TABLE sessions (
  session_id SMALLINT NOT NULL PRIMARY KEY,
  exam_amount TINYINT,
  session_type VARCHAR(10) CHECK (session_type = 'winter' or session_type = 'summer'),
  deducted_number SMALLINT
  );
""")

cursor.executescript("""
INSERT INTO sessions VALUES (1, 5, 'winter', 0);
INSERT INTO sessions VALUES (2, 5, 'summer', 0);
""")

cursor.executescript("""
INSERT INTO departments VALUES (1, 'MATAN DEP', 15, 64);
""")

cursor.executescript("""
INSERT INTO exams VALUES (1, 'MATAN', '2020-01-20', 1, '10 point system', 1);
""")

conn.commit()

