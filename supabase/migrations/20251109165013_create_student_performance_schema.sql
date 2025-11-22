/*
  # Student Performance Analyzer Schema

  1. New Tables
    - `students`
      - `id` (uuid, primary key) - Unique student identifier
      - `name` (text) - Student full name
      - `email` (text, unique) - Student email address
      - `enrollment_date` (date) - Date of enrollment
      - `created_at` (timestamptz) - Record creation timestamp
    
    - `courses`
      - `id` (uuid, primary key) - Unique course identifier
      - `name` (text) - Course name
      - `code` (text, unique) - Course code
      - `credits` (integer) - Number of credits
      - `created_at` (timestamptz) - Record creation timestamp
    
    - `grades`
      - `id` (uuid, primary key) - Unique grade identifier
      - `student_id` (uuid, foreign key) - References students table
      - `course_id` (uuid, foreign key) - References courses table
      - `score` (numeric) - Grade score (0-100)
      - `grade_letter` (text) - Letter grade (A, B, C, D, F)
      - `semester` (text) - Semester information
      - `year` (integer) - Academic year
      - `created_at` (timestamptz) - Record creation timestamp

  2. Security
    - Enable RLS on all tables
    - Add policies for public access (for demo purposes)
    
  3. Notes
    - All tables use UUID primary keys for scalability
    - Foreign key constraints ensure data integrity
    - Indexes added on commonly queried fields
*/

-- Create students table
CREATE TABLE IF NOT EXISTS students (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text UNIQUE NOT NULL,
  enrollment_date date DEFAULT CURRENT_DATE,
  created_at timestamptz DEFAULT now()
);

-- Create courses table
CREATE TABLE IF NOT EXISTS courses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  code text UNIQUE NOT NULL,
  credits integer DEFAULT 3,
  created_at timestamptz DEFAULT now()
);

-- Create grades table
CREATE TABLE IF NOT EXISTS grades (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id uuid NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  course_id uuid NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  score numeric(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
  grade_letter text NOT NULL,
  semester text NOT NULL,
  year integer NOT NULL,
  created_at timestamptz DEFAULT now(),
  UNIQUE(student_id, course_id, semester, year)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_course_id ON grades(course_id);
CREATE INDEX IF NOT EXISTS idx_grades_year ON grades(year);

-- Enable Row Level Security
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (suitable for demo/educational purposes)
CREATE POLICY "Allow public read access to students"
  ON students FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert to students"
  ON students FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update to students"
  ON students FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete from students"
  ON students FOR DELETE
  USING (true);

CREATE POLICY "Allow public read access to courses"
  ON courses FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert to courses"
  ON courses FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update to courses"
  ON courses FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete from courses"
  ON courses FOR DELETE
  USING (true);

CREATE POLICY "Allow public read access to grades"
  ON grades FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert to grades"
  ON grades FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public update to grades"
  ON grades FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow public delete from grades"
  ON grades FOR DELETE
  USING (true);