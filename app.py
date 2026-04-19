from src.database.connect import engine
from src.database.models import Student, Group, Teacher, Subject, Grade
from datetime import datetime


from sqlalchemy import text, select, func
from sqlalchemy.orm import Session

def create_groups( session: Session):
    groups = [
        Group(name="Group A"),
        Group(name="Group B"),
    ]
    session.add_all(groups)
    return groups


def create_teachers(session: Session):
    teachers = [
        Teacher(name="Dr. Smith"),
        Teacher(name="Prof. Johnson"),
    ]
    session.add_all(teachers)
    return teachers

def create_subjects(session: Session, teachers):
    subjects = [
        Subject(name="Math", teacher=teachers[0]),
        Subject(name="Physics", teacher=teachers[1]),
        ]
    session.add_all(subjects)
    return subjects

def create_students(session: Session, groups):
    students = [
        Student(name="Alice", group=groups[0]),
        Student(name="Bob", group=groups[0]),
        Student(name="Charlie", group=groups[1]),
        ]
    session.add_all(students)
    return students

def create_grades(session: Session, students, subjects):
    grades = [
        Grade(student=students[0], subject=subjects[0], grade=95),
            Grade(student=students[0], subject=subjects[1], grade=88),
            Grade(student=students[1], subject=subjects[0], grade=89),
        ]
    session.add_all(grades)
    return grades




if __name__ == '__main__':
    with Session(engine) as session:
        groups = create_groups(session)
        teachers = create_teachers(session)

        session.flush()  

        subjects = create_subjects(session, teachers)
        students = create_students(session, groups)

        session.flush()

        create_grades(session, students, subjects)

        session.commit()
