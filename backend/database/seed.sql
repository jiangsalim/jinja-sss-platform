-- Default Classes
INSERT INTO classes (name, level) VALUES ('S1', 'O-Level');
INSERT INTO classes (name, level) VALUES ('S2', 'O-Level');
INSERT INTO classes (name, level) VALUES ('S3', 'O-Level');
INSERT INTO classes (name, level) VALUES ('S4', 'O-Level');
INSERT INTO classes (name, level) VALUES ('S5', 'A-Level');
INSERT INTO classes (name, level) VALUES ('S6', 'A-Level');

-- Streams for S1-S4
INSERT INTO streams (class_id, stream_code) VALUES (1,'A'),(1,'B'),(1,'C'),(1,'D');
INSERT INTO streams (class_id, stream_code) VALUES (2,'A'),(2,'B'),(2,'C'),(2,'D');
INSERT INTO streams (class_id, stream_code) VALUES (3,'A'),(3,'B'),(3,'C'),(3,'D');
INSERT INTO streams (class_id, stream_code) VALUES (4,'A'),(4,'B'),(4,'C'),(4,'D');

-- Departments
INSERT INTO departments (name) VALUES ('Science'),('Mathematics'),('Languages'),('Humanities'),('Commerce');

-- Subjects
INSERT INTO subjects (name, code, department_id) VALUES ('Mathematics','MATH101',2),('Physics','PHY101',1),('Chemistry','CHE101',1),('English','ENG101',3),('Biology','BIO101',1),('History','HIS101',4),('Geography','GEO101',4),('Commerce','COM101',5);

-- Academic Year
INSERT INTO academic_years (year, start_date, end_date, is_current) VALUES (2026,'2026-01-15','2026-12-10',1);

-- Terms
INSERT INTO terms (academic_year_id, term_number, start_date, end_date, is_active) VALUES (1,1,'2026-01-15','2026-04-05',0),(1,2,'2026-04-15','2026-07-05',1),(1,3,'2026-07-15','2026-10-05',0);

-- System Settings
INSERT INTO system_settings (setting_key, setting_value) VALUES ('school_name','Jinja Senior Secondary School'),('school_motto','Education for Service'),('current_year','2026');

-- Test Admin User (password: admin123)
INSERT INTO users (username, email, password_hash, full_name, role, is_active, first_login) VALUES ('admin','admin@jinjasss.sc.ug','$2b$12$LJ3m4ys3GZfnYMz8kVsKaOTSxGHLfEhCgJwN5VybRqYKXGvL7bHGa','System Admin','admin',1,0);
