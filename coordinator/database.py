"""
Database module for the University Management System.
"""

from sqlalchemy import create_engine, text
import os

db_path = os.path.join(os.path.dirname(__file__), 'university.sqlite')
engine = create_engine(f'sqlite:///{db_path}')

def init_db():
    """Initialize the database with tables and sample data."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                state TEXT NOT NULL,
                type TEXT NOT NULL
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university_course (
                university_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                PRIMARY KEY (university_id, course_id),
                FOREIGN KEY (university_id) REFERENCES university (id),
                FOREIGN KEY (course_id) REFERENCES course (id)
            );
        """))

        conn.execute(text("""
            INSERT INTO university (name, state, type) VALUES
                ('UFRJ', 'RJ', 'public'),
                ('PUC-Rio', 'RJ', 'private'),
                ('USP', 'SP', 'public'),
                ('Unicamp', 'SP', 'public')
            ON CONFLICT DO NOTHING;
        """))

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
    """Get the SQLAlchemy engine instance."""
    return engine
