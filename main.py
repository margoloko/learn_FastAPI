from typing import Dict, List

from fastapi import Body, FastAPI

from schemas import Person


app = FastAPI()


@app.post('/hello')
def greetings(person: Person = Body(...,
                                    examples=Person.Config.schema_extra['examples']             
              )) -> Dict[str, str]:
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