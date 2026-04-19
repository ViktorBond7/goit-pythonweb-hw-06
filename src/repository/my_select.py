from sqlalchemy.orm import Session
from src.database.models import Student, Group, Teacher, Subject, Grade
from src.database.connect import engine
from sqlalchemy import select, func

"""
--Знайти 5 студентів із найбільшим середнім балом з усіх предметів
SELECT 
    s.name, 
    AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.id
GROUP BY s.id, s.name
ORDER BY average_grade DESC
LIMIT 5;

"""


def get_top_students(limit: int = 5):
    with Session(engine) as session:
        sgl = (
            select(Student.name, func.avg(Grade.grade).label("average_grade"))
            .join(Grade)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(limit)
        )
        return session.execute(sgl).fetchall()


"""
--Знайти студента із найвищим середнім балом з певного предмета.

SELECT 
    s.name, 
    AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects sub ON g.subject_id = sub.id
WHERE sub.name = 'Art'
GROUP BY s.id, s.name
ORDER BY average_grade DESC
LIMIT 1;

"""


def get_top_student_by_subject(subject_name: str):
    with Session(engine) as session:
        sgl = (
            select(Student.name, func.avg(Grade.grade).label("average_grade"))
            .join(Grade)
            .join(Subject)
            .where(Subject.name == subject_name)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
        )
        return session.execute(sgl).fetchone()


"""
--Знайти середній бал у групах з певного предмета.

SELECT 
    g2.name AS group_name, 
    AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects sub ON g.subject_id = sub.id
JOIN groups g2 ON s.group_id = g2.id
WHERE sub.name = 'Art'
GROUP BY g2.id, g2.name  -- Group only by the group, not the student
ORDER BY average_grade DESC;

"""


def get_average_grade_by_group_and_subject(subject_name: str):
    with Session(engine) as session:
        sgl = (
            select(
                Group.name.label("group_name"),
                func.avg(Grade.grade).label("average_grade"),
            )
            .select_from(Group)
            .join(Student, Group.id == Student.group_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .where(Subject.name == subject_name)
            .group_by(Group.id, Group.name)  # Group only by the group, not the student
            .order_by(func.avg(Grade.grade).desc())
        )

        return session.execute(sgl).fetchall()


"""
--Знайти середній бал на потоці (по всій таблиці оцінок).

SELECT 
    AVG(grade) AS total_average 
FROM grades;

"""


def get_overall_average_grade():
    with Session(engine) as session:
        sgl = select(func.avg(Grade.grade).label("total_average"))
        return session.execute(sgl).scalar_one()


"""
--Знайти які курси читає певний викладач.

select s.name, t.name from subjects s
join teachers t on s.teacher_id = t.id
where t.name = 'Denise Williams

"""


def get_subjects_by_teacher(teacher_name: str):
    with Session(engine) as session:
        sgl = select(Subject.name).join(Teacher).where(Teacher.name == teacher_name)
        return session.execute(sgl).fetchall()


"""
--Знайти список студентів у певній групі.

select s.id, s.name from students s
join groups g on s.group_id = g.id
where g.name = 'Group A'
order by s.name

"""


def get_students_by_group(group_name: str):
    with Session(engine) as session:
        sgl = (
            select(Student.name)
            .join(Group)
            .where(Group.name == group_name)
            .order_by(Student.name)
        )
        return session.execute(sgl).fetchall()


"""
--Знайти оцінки студентів у окремій групі з певного предмета.

SELECT 
    s.name AS student_name, 
    g.grade, 
    sub.name AS subject_name,
    gr.name AS group_name
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects sub ON g.subject_id = sub.id
JOIN groups gr ON s.group_id = gr.id
WHERE gr.name = 'Group A' AND sub.name = 'Art'
ORDER BY s.name;

"""


def get_grades_by_group_and_subject(group_name: str, subject_name: str):
    with Session(engine) as session:
        sgl = (
            select(
                Student.name.label("student_name"),
                Grade.grade,
                Subject.name.label("subject_name"),
                Group.name.label("group_name"),
            )
            .select_from(Student)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .join(Group, Student.group_id == Group.id)
            .where(Group.name == group_name, Subject.name == subject_name)
            .order_by(Student.name)
        )
        return session.execute(sgl).fetchall()


"""
--Знайти середній бал, який ставить певний викладач зі своїх предметів.

select 
	t.name AS teacher_name, 
	AVG(g.grade) AS average_grade 
	from grades g
join subjects s on g.subject_id = s.id 
join teachers t on s.teacher_id = t.id
where t.name = 'Denise Williams'
group by t.id, t.name

"""


def get_average_grade_by_teacher(teacher_name: str):
    with Session(engine) as session:
        sgl = (
            select(
                Teacher.name.label("teacher_name"),
                func.avg(Grade.grade).label("average_grade"),
            )
            .join(Subject, Teacher.id == Subject.teacher_id)
            .join(Grade, Subject.id == Grade.subject_id)
            .where(Teacher.name == teacher_name)
            .group_by(Teacher.id, Teacher.name)
        )
        return session.execute(sgl).fetchone()


"""
--Знайти список курсів, які відвідує певний студент.

SELECT DISTINCT 
    s2.name AS subject_name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects s2 ON g.subject_id = s2.id
WHERE s.name = 'Emily Schwartz'
ORDER BY s2.name;

"""


def get_subjects_by_student(student_name: str):
    with Session(engine) as session:
        sgl = (
            select(Subject.name.label("subject_name"))
            .distinct()
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .where(Student.name == student_name)
            .order_by(Subject.name)
        )
        return session.execute(sgl).fetchall()


"""
--Список курсів, які певному студенту читає певний викладач.

select DISTINCT
	s.name, 
	s2.name, 
	t.name    
from subjects s 
join teachers t on s.teacher_id = t.id 
join grades g on g.subject_id = s.id
join students s2 on g.student_id = s2.id 
where t.name = 'Denise Williams' and s2.name = 'Emily Schwartz'

"""


def get_subjects_by_student_and_teacher(student_name: str, teacher_name: str):
    with Session(engine) as session:
        sgl = (
            select(Subject.name.label("subject_name"))
            .distinct()
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .where(Teacher.name == teacher_name, Student.name == student_name)
        )
        return session.execute(sgl).fetchall()


if __name__ == "__main__":
    # print(get_top_students())
    # print(get_top_student_by_subject("Art"))
    # print(get_average_grade_by_group_and_subject("Art"))
    # print(get_overall_average_grade())
    # print(get_subjects_by_teacher("Denise Williams"))
    # print(get_students_by_group("Group A"))
    # print(get_grades_by_group_and_subject("Group A", "Art"))
    # print(get_average_grade_by_teacher("Denise Williams"))
    # print(get_subjects_by_student("Emily Schwartz"))
    print(get_subjects_by_student_and_teacher("Emily Schwartz", "Denise Williams"))
