from sqlalchemy import create_engine, text
import os

# Database will be created in coordinator directory
db_path = os.path.join(os.path.dirname(__file__), 'university.sqlite')
engine = create_engine(f'sqlite:///{db_path}')

def init_db():
    with engine.begin() as conn:
        # Universities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                state TEXT NOT NULL,
                type TEXT NOT NULL,
                founded_year INTEGER,
                student_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Sample data
        conn.execute(text("""
            INSERT INTO university (name, state, type, founded_year, student_count) VALUES
                ('UFRJ', 'RJ', 'public', 1920, 45000),
                ('PUC-Rio', 'RJ', 'private', 1941, 23000),
                ('USP', 'SP', 'public', 1934, 60000),
                ('Unicamp', 'SP', 'public', 1966, 37000)
            ON CONFLICT DO NOTHING;
        """))

        # Courses table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                duration_years INTEGER DEFAULT 4,
                area TEXT NOT NULL
            );
        """))

        conn.execute(text("""
            INSERT INTO course (name, duration_years, area) VALUES
                ('Ciência da Computação', 4, 'Exatas'),
                ('Engenharia de Software', 4, 'Exatas'),
                ('Medicina', 6, 'Saúde'),
                ('Direito', 5, 'Humanas'),
                ('Biologia', 4, 'Biológicas'),
                ('História', 4, 'Humanas'),
                ('Matemática', 4, 'Exatas')
            ON CONFLICT DO NOTHING;
        """))

        # University-Course relationship
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university_course (
                university_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                annual_spots INTEGER DEFAULT 50,
                tuition_fee DECIMAL(10,2) DEFAULT 0.00,
                PRIMARY KEY (university_id, course_id),
                FOREIGN KEY (university_id) REFERENCES university (id),
                FOREIGN KEY (course_id) REFERENCES course (id)
            );
        """))

        # Students table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                university_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrollment_year INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (university_id) REFERENCES university (id),
                FOREIGN KEY (course_id) REFERENCES course (id)
            );
        """))

def get_engine():
    return engine
