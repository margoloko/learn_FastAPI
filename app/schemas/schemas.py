import re

from enum import Enum
from typing import Optional, Dict, List, Union
from pydantic import BaseModel, Field, root_validator, validator


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    """
    Класс для представления человека.

    :param name: полное имя
    :type name: str
    :param surname: фамилия или список фамилий
    :type surname: Union[str, List[str]]
    :param age: возраст
    :type age: Optional[int]
    :param is_staff: является ли сотрудником
    :type is_staff: bool
    :param education_level: уровень образования
    :type education_level: Optional[EducationLevel]
    """
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
        schema_extra = {
            'examples': {
                'single_surname': {
                    'summary': 'Одна фамилия',
                    'description': 'Одиночная фамилия передается строкой',
                    'value': {
                       'name': 'Taras',
                       'surname': 'Belov',
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Среднее образование'
                    }
                },
                'multiple_surnames': {
                    'summary': 'Несколько фамилий',
                    'description': 'Несколько фамилий передаются списком',
                    'value': {
                       'name': 'Eduardo',
                       'surname': ['Santos', 'Tavares'],
                       'age': 20,
                       'is_staff': False,
                       'education_level': 'Высшее образование'
                    }
                },
                'invalid': {
                    'summary': 'Некорректный запрос',
                    'description': 'Возраст передается только целым числом',
                    'value': {
                        'name': 'Eduardo',
                        'surname': ['Santos', 'Tavares'],
                        'age': 'forever young',
                        'is_staff': False,
                        'education_level': 'Среднее специальное образование'
                    }
                }
            }
        }

    @validator('name')
    def name_cant_be_numeric(cls, value: str):
        """
        Валидатор для проверки имени на наличие цифр.

        :param value: значение имени
        :type value: str
        :return: значение имени (если оно не содержит цифр)
        :rtype: str
        """
        if value.isnumeric():
            raise ValueError('not chislo')
        return value
    
    @root_validator(skip_on_failure=True)
    def using_different_languages(cls, values):
        """
        Валидатор для проверки использования разных языков в имени и фамилии.

        :param values: значения полей модели
        :type values: dict
        :return: значения полей модели (если имя и фамилия используют только латиницу или только кириллицу)
        :rtype: dict
        """
        surname = ''.join(values['surname'])
        checked_value = values['name'] + surname
        if (re.search('[а-я]', checked_value, re.IGNORECASE)
        and re.search('[a-z]', checked_value, re.IGNORECASE)):
            raise ValueError('tolko latin or cirill')
        return values
