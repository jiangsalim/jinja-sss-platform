-- Jinja SSS Platform - Complete Database Schema
-- 73 Tables

PRAGMA foreign_keys = ON;

-- ============================================
-- CORE USER MANAGEMENT
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    phone TEXT,
    profile_picture TEXT,
    is_active BOOLEAN DEFAULT 1,
    first_login BOOLEAN DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    device_type TEXT,
    device_name TEXT,
    ip_address TEXT,
    last_active DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS login_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    device_type TEXT,
    success BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- ACADEMIC STRUCTURE
-- ============================================

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level TEXT,
    capacity INTEGER DEFAULT 45,
    current_enrollment INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS streams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    stream_code TEXT NOT NULL,
    student_count INTEGER DEFAULT 0,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    budget DECIMAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    department_id INTEGER,
    is_elective BOOLEAN DEFAULT 0,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS academic_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    academic_year_id INTEGER NOT NULL,
    term_number INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT 0,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id)
);


-- ============================================
-- STUDENTS
-- ============================================

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    admission_number TEXT UNIQUE NOT NULL,
    class_id INTEGER,
    stream_id INTEGER,
    date_of_birth DATE,
    gender TEXT,
    blood_group TEXT,
    medical_conditions TEXT,
    enrollment_year INTEGER,
    is_transfer BOOLEAN DEFAULT 0,
    previous_school TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (stream_id) REFERENCES streams(id)
);

CREATE TABLE IF NOT EXISTS student_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    document_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    verified BOOLEAN DEFAULT 0,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ============================================
-- TEACHERS & STAFF
-- ============================================

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    staff_id TEXT UNIQUE NOT NULL,
    teacher_type TEXT DEFAULT 'subject',
    department_id INTEGER,
    qualification TEXT,
    specialization TEXT,
    joining_date DATE,
    mentor_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (mentor_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS teacher_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    class_id INTEGER,
    stream_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (stream_id) REFERENCES streams(id)
);

CREATE TABLE IF NOT EXISTS staff_leave (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    leave_type TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    approved_by INTEGER,
    approved_at DATETIME,
    FOREIGN KEY (staff_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS staff_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT DEFAULT 'present',
    check_in TIME,
    check_out TIME,
    FOREIGN KEY (staff_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS performance_appraisals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    appraiser_id INTEGER,
    term_id INTEGER,
    lesson_preparation INTEGER DEFAULT 0,
    content_delivery INTEGER DEFAULT 0,
    student_engagement INTEGER DEFAULT 0,
    classroom_management INTEGER DEFAULT 0,
    overall_rating REAL DEFAULT 0,
    strengths TEXT,
    areas_for_improvement TEXT,
    status TEXT DEFAULT 'draft',
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (term_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    trainer_id INTEGER,
    session_date DATETIME,
    venue TEXT,
    FOREIGN KEY (trainer_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS training_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_id INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    attended BOOLEAN DEFAULT 0,
    FOREIGN KEY (training_id) REFERENCES training_sessions(id),
    FOREIGN KEY (staff_id) REFERENCES teachers(id)
);

-- ============================================
-- GRADES & ATTENDANCE
-- ============================================

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    exam_type TEXT NOT NULL,
    term_id INTEGER,
    score REAL NOT NULL,
    grade TEXT,
    remarks TEXT,
    recorded_by INTEGER,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'submitted',
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (term_id) REFERENCES terms(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    class_id INTEGER,
    stream_id INTEGER,
    date DATE NOT NULL,
    period INTEGER DEFAULT 1,
    status TEXT DEFAULT 'present',
    marked_by INTEGER,
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (marked_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS homework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    class_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS homework_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    homework_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT,
    score REAL,
    feedback TEXT,
    status TEXT DEFAULT 'submitted',
    FOREIGN KEY (homework_id) REFERENCES homework(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS lesson_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    class_id INTEGER,
    week INTEGER,
    topic TEXT NOT NULL,
    objectives TEXT,
    activities TEXT,
    resources TEXT,
    status TEXT DEFAULT 'pending',
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    stream_id INTEGER,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    day_of_week INTEGER,
    start_time TIME,
    end_time TIME,
    room TEXT,
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS student_transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    from_class_id INTEGER,
    to_class_id INTEGER,
    from_stream_id INTEGER,
    to_stream_id INTEGER,
    transfer_date DATE,
    reason TEXT,
    approved_by INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================
-- PARENTS
-- ============================================

CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    occupation TEXT,
    relationship_type TEXT,
    emergency_contact BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS parent_student_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    is_verified BOOLEAN DEFAULT 0,
    can_pay_fees BOOLEAN DEFAULT 1,
    can_view_grades BOOLEAN DEFAULT 1,
    FOREIGN KEY (parent_id) REFERENCES parents(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================
-- FINANCE
-- ============================================

CREATE TABLE IF NOT EXISTS fee_structure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    tuition_fee DECIMAL DEFAULT 0,
    activity_fee DECIMAL DEFAULT 0,
    library_fee DECIMAL DEFAULT 0,
    sports_fee DECIMAL DEFAULT 0,
    development_fee DECIMAL DEFAULT 0,
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (term_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS fee_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    term_id INTEGER,
    amount DECIMAL NOT NULL,
    payment_method TEXT,
    transaction_id TEXT,
    payment_date DATE DEFAULT CURRENT_DATE,
    receipt_number TEXT UNIQUE,
    recorded_by INTEGER,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (term_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS parent_fee_balance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    total_fees DECIMAL DEFAULT 0,
    amount_paid DECIMAL DEFAULT 0,
    balance DECIMAL DEFAULT 0,
    due_date DATE,
    payment_status TEXT DEFAULT 'pending',
    FOREIGN KEY (parent_id) REFERENCES parents(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (term_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount DECIMAL NOT NULL,
    description TEXT,
    vendor TEXT,
    expense_date DATE DEFAULT CURRENT_DATE,
    approved_by INTEGER,
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    fiscal_year INTEGER NOT NULL,
    allocated DECIMAL DEFAULT 0,
    spent DECIMAL DEFAULT 0,
    remaining DECIMAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS payroll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    basic_salary DECIMAL DEFAULT 0,
    allowances TEXT,
    deductions TEXT,
    net_pay DECIMAL DEFAULT 0,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (staff_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    invoice_number TEXT UNIQUE,
    amount DECIMAL NOT NULL,
    issued_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    status TEXT DEFAULT 'issued',
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (term_id) REFERENCES terms(id)
);

-- ============================================
-- COMMUNICATION
-- ============================================

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant1_id INTEGER NOT NULL,
    participant2_id INTEGER NOT NULL,
    last_message TEXT,
    last_message_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant1_id) REFERENCES users(id),
    FOREIGN KEY (participant2_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    attachment_url TEXT,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    priority TEXT DEFAULT 'normal',
    target_roles TEXT,
    target_classes TEXT,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    target_department TEXT,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (reporter_id) REFERENCES users(id)
);

-- ============================================
-- DISCIPLINE
-- ============================================

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    description TEXT,
    severity TEXT DEFAULT 'minor',
    reported_by INTEGER,
    reported_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    resolution TEXT,
    resolved_by INTEGER,
    resolved_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (reported_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sanctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    student_id INTEGER NOT NULL,
    sanction_type TEXT NOT NULL,
    duration_days INTEGER DEFAULT 0,
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (incident_id) REFERENCES incidents(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS behavior_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    plan_type TEXT,
    goals TEXT,
    start_date DATE,
    end_date DATE,
    progress INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================
-- HEALTH & MEDICAL
-- ============================================

CREATE TABLE IF NOT EXISTS student_medical_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL UNIQUE,
    blood_group TEXT,
    allergies TEXT,
    chronic_conditions TEXT,
    medications TEXT,
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS sick_bay_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    arrival_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    symptoms TEXT,
    diagnosis TEXT,
    treatment TEXT,
    medication_given TEXT,
    disposition TEXT DEFAULT 'returned_to_class',
    departure_time DATETIME,
    nurse_id INTEGER,
    parent_notified BOOLEAN DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (nurse_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS medication_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    medication_name TEXT NOT NULL,
    dosage TEXT,
    frequency TEXT,
    administration_time TIME,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS counseling_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_type TEXT DEFAULT 'individual',
    reason TEXT,
    notes TEXT,
    follow_up_date DATETIME,
    counselor_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (counselor_id) REFERENCES users(id)
);

-- ============================================
-- LIBRARY
-- ============================================

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT,
    title TEXT NOT NULL,
    author TEXT,
    publisher TEXT,
    year INTEGER,
    category TEXT,
    quantity INTEGER DEFAULT 1,
    available INTEGER DEFAULT 1,
    location TEXT
);

CREATE TABLE IF NOT EXISTS book_loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    borrow_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    return_date DATE,
    status TEXT DEFAULT 'borrowed',
    fine_amount DECIMAL DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS book_reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    reservation_date DATE DEFAULT CURRENT_DATE,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- ============================================
-- TRANSPORT
-- ============================================

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration TEXT UNIQUE NOT NULL,
    model TEXT,
    capacity INTEGER DEFAULT 60,
    type TEXT DEFAULT 'bus',
    status TEXT DEFAULT 'active',
    fuel_efficiency REAL,
    last_service DATE,
    next_service DATE
);

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stops TEXT,
    distance REAL,
    estimated_duration INTEGER
);

CREATE TABLE IF NOT EXISTS bus_students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    pickup_stop TEXT,
    dropoff_stop TEXT,
    active BOOLEAN DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- ============================================
-- VOTING
-- ============================================

CREATE TABLE IF NOT EXISTS voting_elections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATETIME,
    end_date DATETIME,
    is_active BOOLEAN DEFAULT 0,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS voting_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    election_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (election_id) REFERENCES voting_elections(id)
);

CREATE TABLE IF NOT EXISTS voting_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    manifesto TEXT,
    FOREIGN KEY (position_id) REFERENCES voting_positions(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS voting_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    election_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    stream_id INTEGER,
    vote_count INTEGER DEFAULT 0,
    recorded_by INTEGER,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (election_id) REFERENCES voting_elections(id),
    FOREIGN KEY (candidate_id) REFERENCES voting_candidates(id)
);

-- ============================================
-- SYSTEM & AUDIT
-- ============================================

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    resource TEXT,
    resource_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS backup_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_file TEXT NOT NULL,
    backup_size INTEGER,
    status TEXT DEFAULT 'success',
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    api_key TEXT UNIQUE NOT NULL,
    name TEXT,
    permissions TEXT,
    last_used DATETIME,
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS email_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME
);

-- ============================================
-- PREFTECTS
-- ============================================

CREATE TABLE IF NOT EXISTS prefects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL UNIQUE,
    prefect_type TEXT NOT NULL,
    department TEXT,
    appointed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS prefect_duties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prefect_id INTEGER NOT NULL,
    location TEXT,
    day_of_week INTEGER,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (prefect_id) REFERENCES prefects(id)
);

CREATE TABLE IF NOT EXISTS prefect_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prefect_id INTEGER NOT NULL,
    report_date DATE DEFAULT CURRENT_DATE,
    content TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prefect_id) REFERENCES prefects(id)
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_students_admission ON students(admission_number);
CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);
CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_fee_payments_student ON fee_payments(student_id);
CREATE INDEX IF NOT EXISTS idx_incidents_student ON incidents(student_id);
CREATE INDEX IF NOT EXISTS idx_book_loans_student ON book_loans(student_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit_log(created_at);

-- ============================================
-- MISSING TABLES (8)
-- ============================================

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    level INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    resource TEXT,
    action TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS appeals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sanction_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    decision TEXT,
    decided_by INTEGER,
    decided_at DATETIME,
    FOREIGN KEY (sanction_id) REFERENCES sanctions(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS welfare_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    case_type TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'active',
    social_worker_id INTEGER,
    opened_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS home_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    student_id INTEGER NOT NULL,
    visit_date DATE DEFAULT CURRENT_DATE,
    findings TEXT,
    actions_taken TEXT,
    next_visit_date DATE,
    conducted_by INTEGER,
    FOREIGN KEY (case_id) REFERENCES welfare_cases(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS parent_complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    student_id INTEGER,
    subject TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    response TEXT,
    resolved_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (parent_id) REFERENCES parents(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS health_screenings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    screening_type TEXT NOT NULL,
    screening_date DATE DEFAULT CURRENT_DATE,
    results TEXT,
    referred BOOLEAN DEFAULT 0,
    conducted_by INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
