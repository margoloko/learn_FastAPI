# main.py
from enum import Enum
from typing import Optional, Dict, List, Union

from fastapi import FastAPI
# Для работы с JSON в теле запроса 
# импортируем из pydantic класс BaseModel
from pydantic import BaseModel

app = FastAPI()


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'



class Person(BaseModel):
    name: str
    surname: Union[str, List[str]]
    age: Optional[int]
    is_staff: bool = False
    education_level: Optional[EducationLevel]


@app.post('/hello')
def greetings(person: Person) -> Dict[str, str]:
    if isinstance(person.surname, List):
        surnames = ' '.join(person.surname)
    else:
        surname = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()    
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}