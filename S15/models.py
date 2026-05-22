import os
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    BooleanField,
    ForeignKeyField
)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
db = SqliteDatabase(DB_PATH, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Teacher(BaseModel):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    middle_name = CharField(max_length=50)
    is_active = BooleanField(default=True)

    class Meta:
        indexes = (
            (("first_name", "last_name", "middle_name"), True),
        )


class Group(BaseModel):
    name = CharField(max_length=20, unique=True)
    is_active = BooleanField(default=True)


class Discipline(BaseModel):
    name = CharField(max_length=100, unique=True)
    is_active = BooleanField(default=True)


class Assignment(BaseModel):
    teacher = ForeignKeyField(Teacher, backref="assignments", on_delete="CASCADE")
    group = ForeignKeyField(Group, backref="assignments", on_delete="CASCADE")
    discipline = ForeignKeyField(Discipline, backref="assignments", on_delete="CASCADE")
    is_active = BooleanField(default=True)

    class Meta:
        indexes = (
            (("teacher", "group", "discipline"), True),
        )


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Teacher, Group, Discipline, Assignment], safe=True)
    db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")