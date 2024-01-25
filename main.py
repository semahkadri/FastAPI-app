from typing import Optional
from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel


app = FastAPI()

DATABASE_URL = "postgresql://semah:semah@postgres-container:5432/semah"


def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


conn = get_connection()


def create_table():
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                age INTEGER
            );
            """
        )
        print("Table created successfully")

    conn.commit()


create_table()


class Person(BaseModel):
   # id: Optional[int] = None
    first_name: str
    last_name: str
    age: int


def create_person(person: Person):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO people (first_name, last_name, age) VALUES (%s, %s, %s) RETURNING id;",
            (person.first_name, person.last_name, person.age),
        )
        person_id = cursor.fetchone()[0]
        conn.commit()
        return Person(
            id=person_id,
            first_name=person.first_name,
            last_name=person.last_name,
            age=person.age,
        )


def get_people():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM people;")
        people = (
            cursor.fetchall()
        )
        return [
            {"id": p[0], "first_name": p[1], "last_name": p[2], "age": p[3]}
            for p in people
        ]


@app.post("/people", response_model=Person)
async def create_person_api(person: Person):
    return create_person(person)


@app.get("/people", response_model=list[Person])
async def get_people_api():
    return get_people()


class DeletedPersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int


@app.delete("/people/{person_id}", response_model=DeletedPersonResponse)
def delete_person(person_id: int):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id , first_name , last_name , age FROM people WHERE id = %s; ",
            (person_id,),
        )
        existing_person = cursor.fetchone()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=406, detail="Person not available")
        deleted_person = DeletedPersonResponse(
            id=existing_person[0],
            first_name=existing_person[1],
            last_name=existing_person[2],
            age=existing_person[3],
        )

        cursor.execute("DELETE FROM people where id = %s;", (person_id,))
        conn.commit()

        return deleted_person


class UpdatedPersonRequest(BaseModel):
    first_name: str = ...
    last_name: str = ...
    age: int = ...


class UpdatedPersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int


@app.put("/people/{person_id}", response_model=UpdatedPersonResponse)
def update_person(person_id=int, updated_person: UpdatedPersonRequest = None):
    if not updated_person or len(updated_person.dict()) == 0:
        raise HTTPException(status_code=422, detail="EMPTY REQUEST BODY")

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE people SET first_name = %s , last_name = %s , age = %s WHERE id = %s RETURNING id , first_name , last_name , age ;",
            (
                updated_person.first_name,
                updated_person.last_name,
                updated_person.age,
                person_id,
            ),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=406, detail="Person not available")

        return UpdatedPersonResponse(
            id=person_id,
            first_name=updated_person.first_name,
            last_name=updated_person.last_name,
            age=updated_person.age,
        )
