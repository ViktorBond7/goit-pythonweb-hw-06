from sqlalchemy import ForeignKey, String, Boolean, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Student({self.id}, {self.name})"

    def __repr__(self):
        return str(self)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    students: Mapped[list["Student"]] = relationship(back_populates="group")



    # group = relationship(back_populates="students")


    def __str__(self):
        return f"Group({self.id}, {self.name})"

    def __repr__(self):
        return str(self)


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

    def __str__(self):
        return f"Teacher({self.id}, {self.name})"

    def __repr__(self):
        return str(self)


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"Subject({self.id}, {self.name})"

    def __repr__(self):
        return str(self)


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    def __str__(self):
        return f'Grade({self.id}, {self.student.name}, {self.subject.name}, {self.grade})'

    def __repr__(self):
        return str(self)
