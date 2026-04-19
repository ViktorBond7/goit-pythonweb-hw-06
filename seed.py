from src.database.models import Group, Teacher, Subject, Student, Grade
from src.database.connect import engine
from sqlalchemy.orm import Session
import random

from faker import Faker

fake = Faker()

GROUPS = ["Group A", "Group B", "Group C"]
SUBJECT = [
    "Math",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Literature",
    "Art",
    "Music",
]


def seed_data(session):
    # clear existing data
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()

    # create groups
    groups = [Group(name=name) for name in GROUPS]
    session.add_all(groups)

    # create teachers
    teachers = [Teacher(name=fake.name()) for _ in range(5)]
    session.add_all(teachers)

    session.flush()

    # create subjects and assign them to random teachers
    subjects = [Subject(name=name, teacher=random.choice(teachers)) for name in SUBJECT]
    session.add_all(subjects)
    session.flush()

    # create students and assign them to random groups
    students = [
        Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)
    ]
    session.add_all(students)
    session.flush()

    # create grades end create random grades for students and subjects
    for student in students:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.randint(1, 100),
            )
            session.add(grade)

    session.commit()


if __name__ == "__main__":
    with Session(engine) as session:
        seed_data(session)
