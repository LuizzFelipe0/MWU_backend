import re

from fastapi import HTTPException


def cpf_validator(cpf: str) -> str:
    # Remove everything that is not a number
    cpf = re.sub(r'\D', '', cpf)

    # CPF has to be 11 digits
    if len(cpf) != 11:
        raise HTTPException(status_code=422, detail='Invalid CPF format! CPF has to be 11 digits')

    # Repeated sequences like 11111111111 are not allowed
    if cpf == cpf[0] * 11:
        raise HTTPException(status_code=422, detail='Invalid CPF format! Repeated sequences are not allowed')

    # Validation of first digit
    cpf_sum = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = (cpf_sum * 10) % 11
    if first_digit == 10:
        first_digit = 0

    if first_digit != int(cpf[9]):
        raise HTTPException(status_code=422, detail='Invalid CPF format! First digit rule is incorrect')

    # Validation of second digit
    cpf_sum = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = (cpf_sum * 10) % 11
    if second_digit == 10:
        second_digit = 0

    if second_digit != int(cpf[10]):
        raise HTTPException(status_code=422, detail='Invalid CPF format! Second digit rule is incorrect')

    return cpf
