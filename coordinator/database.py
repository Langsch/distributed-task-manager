"""
Database module for the University Management System.

This module handles database initialization, table creation, and provides
the SQLAlchemy engine for database operations.
"""

from sqlalchemy import create_engine, text
import os

# Database will be created in coordinator directory
db_path = os.path.join(os.path.dirname(__file__), 'university.sqlite')
engine = create_engine(f'sqlite:///{db_path}')

def init_db():
    """
    Initialize the database with required tables and sample data.
    
    Creates:
    - university table: stores university information
    - course table: stores available courses 
    - university_course table: many-to-many relationship between universities and courses
    
    Also populates sample data for testing.
    """
    with engine.begin() as conn:
        # Universities table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                state TEXT NOT NULL,
                type TEXT NOT NULL
            );
        """))

        # Courses table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """))

        # University-Course relationship
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university_course (
                university_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                PRIMARY KEY (university_id, course_id),
                FOREIGN KEY (university_id) REFERENCES university (id),
                FOREIGN KEY (course_id) REFERENCES course (id)
            );
        """))

        # Sample universities
        conn.execute(text("""
            INSERT INTO university (name, state, type) VALUES
                ('UFRJ', 'RJ', 'public'),
                ('PUC-Rio', 'RJ', 'private'),
                ('USP', 'SP', 'public'),
                ('Unicamp', 'SP', 'public')
            ON CONFLICT DO NOTHING;
        """))

        # Sample courses (fixed list as specified)
        conn.execute(text("""
            INSERT INTO course (name) VALUES
                ('Ciência da computação'),
                ('Biologia'),
                ('História'),
                ('Direito'),
                ('Medicina')
            ON CONFLICT DO NOTHING;
        """))

def get_engine():
    """
    Get the SQLAlchemy engine instance.
    
    Returns:
        Engine: SQLAlchemy engine configured for the university database
    """
    return engine
