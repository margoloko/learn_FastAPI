import re

from enum import Enum
from typing import Optional, Dict, List, Union
from pydantic import BaseModel, Field, root_validator, validator


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str = Field(...,
                      max_lenght=50,
                      title='Полное имя',
                      description='Можно вводить в любом регистре')
    surname: Union[str, List[str]] = Field(...,                                           
                                           max_lenght=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is-staff')
    education_level: Optional[EducationLevel]


    class Config:
        title = 'Класс для приветствия'
        min_anystr_length = 2

    @validator('name')
    def name_cant_be_numeric(cls, value: str):
        if value.isnumeric():
            raise ValueError('not chislo')
        return value
    
    @root_validator(skip_on_failure=True)
    def using_different_languages(cls, values):
        surname = ''.join(values['surname'])
        checked_value = values['name'] + surname
        if (re.search('[а-я]', checked_value, re.IGNORECASE)
        and re.search('[a-z]', checked_value, re.IGNORECASE)):
            raise ValueError('tolko latin or cirill')
        return values
