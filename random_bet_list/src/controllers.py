from urllib.parse import parse_qs
from src.templates import render_templates
from src.validations import random_result, check_result, valid_bet
from src.models.data import GAMEDAYS, SCOREBOARDS


def home(environ: dict) -> str:
    return render_templates("src/views/index.html")


def gamedays(environ: dict) -> str:
    """
    Retrieve information about game days based on the query parameters.
    Uses game_info() and gamedays_list() functions.

    Based on presence of "n", returns an HTML content representing game information, 
    a 404 page, or a list of game days.
    """

    qs_dict: dict[str, str] = parse_qs(environ["QUERY_STRING"])
    maximum: int = len(GAMEDAYS)
    if "n" in qs_dict and qs_dict["n"][0].isnumeric():
        if int(qs_dict["n"][0]) <= maximum and int(qs_dict["n"][0]) > 0:
            return game_info(int(qs_dict["n"][0]))
        else:
            context: dict = {"gameday": int(qs_dict["n"][0])}
            return render_templates("src/views/404_n.html", context)
    else:
        return gamedays_list()


def game_info(n) -> str:
    """
        Display information about games on a specific gameday.
        Used in gamedays() function.
        """

    context: dict[str, str] = {
        "gameday": GAMEDAYS[n-1]["gameday"],
    }

    for i, game in enumerate(GAMEDAYS[n-1]["games"]):
        key: str = f"game{i+1}"
        team1: str = game["team1"]
        team2: str = game["team2"]
        context[key] = f"<td>{team1}</td><td>{team2}</td>"

    return render_templates("src/views/games.html", context)


def gamedays_list() -> str:
    """
    Displays a list of gamedays. Used in gamedays() function.
    """

    games_list: list[int] = []

    for i in GAMEDAYS:
        games_list.append(i["gameday"])

    game_string: str = "<ul>"

    for game in games_list:
        game_string += f"<li><a href='/gamedays/?n={game}'>Jornada {game}</a></li>"

    game_string += "</ ul>"

    context: list = {
        "gamedays_list": game_string
    }

    return render_templates("src/views/gamedays.html", context)


def game_day(environ: dict) -> str:
    """
    A function responsible for route the programm depending on the parameters in URL.
    If bets and gameday are present, then it launches gameday_with_bet_result() passing
    the environ dict. Otherwise, it returns the random_bet_list() function.
    """

    qs_dict: dict[str, str] = parse_qs(environ["QUERY_STRING"])

    if "bets" in qs_dict and "gameday" in qs_dict:
        len_bets_qs: int = len(qs_dict["bets"])
        len_gameday_qs: int = len(qs_dict["gameday"])

        # Necessary in order to check if what is behind "gameday" is an int.
        # Otherwice, if is a str, it will launch Server Error.
        try:
            game_number: int = int(qs_dict["gameday"][0]) - 1
        except ValueError:
            return render_templates("src/views/404.html")

        if 0 <= game_number < len(GAMEDAYS):
            len_games: int = len(GAMEDAYS[game_number]["games"])
        else:
            return render_templates("src/views/404.html")

        if len_bets_qs != len_games and len_gameday_qs != 1 and not valid_bet(qs_dict["bets"]):
            print("hola")
            return render_templates("src/views/404.html")
        else:
            return gameday_with_bet_result(qs_dict)
    else:
        return random_bet_list()


def random_bet_list() -> str:
    """
    Function responsible for displaying the page with a gameday which 
    has not been played yet, and assign a random bet for each game. 
    """

    first_game_not_played: int = -1
    result: str = ""

    for game in GAMEDAYS:
        if game["played"] is False and first_game_not_played == -1:
            first_game_not_played = game["gameday"] - 1

    context: dict[str, str] = {
        "gameday_number": GAMEDAYS[first_game_not_played]["gameday"]
    }

    for i, game in enumerate(GAMEDAYS[first_game_not_played]["games"]):
        result = random_result()
        key: str = f"game{i + 1}"
        team1: str = game["team1"]
        team2: str = game["team2"]
        context[key] = f"<td>{team1}</td><td>{team2}</td><td>{result}</td>"
        key_bet: str = f"bet{i+1}"
        context[key_bet] = result
        context["gameday"] = first_game_not_played + 1
    if first_game_not_played == -1:
        return render_templates("src/views/404_random.html")
    else:
        return render_templates("src/views/random_list_result.html", context)


def gameday_with_bet_result(qs_dict: dict[str, str]) -> str:
    """
    Function that displays the outcomes of submitted bets for a specific gameday.
    """

    game_number: int = int(qs_dict["gameday"][0])-1
    context: dict[str, str] = {
        "gameday_number": GAMEDAYS[game_number]["gameday"]
    }
    for i, game in enumerate(GAMEDAYS[game_number]["games"]):
        key: str = f"game{i+1}"
        bet: int = qs_dict["bets"][i]
        team1: str = game["team1"]
        team2: str = game["team2"]
        score_team1: int = SCOREBOARDS[game_number]["scoreboard"][i][0]
        score_team2: int = SCOREBOARDS[game_number]["scoreboard"][i][1]
        result: tuple = f"{score_team1} - {score_team2}"
        bet_success = check_result(score_team1, score_team2, bet)
        context[key] = (
            f"<td>{team1}</td>"
            f"<td>{team2}</td>"
            f"<td>{bet}</td>"
            f"<td>{result}</td>"
            f"<td>{bet_success}</td>"
        )

    return render_templates("src/views/randombetlist.html", context)
