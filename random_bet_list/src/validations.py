from random import randint


def random_result() -> str | int:
    possible_results: list[int | str] = [1, 2, "X"]
    random_result: int = randint(0, 2)

    return possible_results[random_result]


def check_result(result_team1, result_team2, bet) -> str:
    # Could return bool as well.
    result: str = ""

    if result_team1 == result_team2:
        result = "X"
    elif result_team1 > result_team2:
        result = "1"
    else:
        result = "2"

    if str(result) == str(bet):
        return "SI"
    else:
        return "NO"


def valid_bet(parameters: list[str]) -> bool:
    valid_parameters: list[str | int] = [1, 2, "X"]
    for i, value in enumerate(parameters):
        if value.isalpha():
            parameters[i] = value.upper()
        else:
            parameters[i] = int(value)
        if parameters[i] not in valid_parameters:
            return False

    return True
