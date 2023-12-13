"""
The game of "HangMan"!
"""

import unicodedata
import random
from src.view.gallow import (
    ui_show_info, ui_hint, ui_gallow, ui_letters, ui_ask, ui_game_over,
    ui_error, ui_win
)

# All sentences from sentences.txt are loaded to the list "sentences".
sentences = []

# Here are strored the used/introduced letters by user.
used_letters = []

try:
    with open("src/assets/sentences.txt", 'r') as file:
        for phrase in file:
            sentences.append(phrase.strip())
    # file.close()
except FileNotFoundError as _e:
    ui_error()


def pick_phrase(phrases: list[str]) -> str:
    random_index: int = random.randint(0, len(sentences))
    random_phrase: str = sentences[random_index]
    return random_phrase


def code_random_sentence(sentence: str) -> str:
    """
    Function that encodes the random sentence so the player does not
    see the phrase he/she has to guess.
    """
    coded_sentence: str = ""
    for letter in sentence:
        if letter.isalpha():
            coded_sentence += "_"
        else:
            coded_sentence += letter
    return coded_sentence


def check_letter(letter: str, sentence: str):
    """
    Cheks if the letter is in the phrase.
    """
    is_there: bool = False
    for alpha in sentence:
        if reduce_to_basic(letter).lower() == reduce_to_basic(alpha).lower():
            is_there = True
    return is_there


def reduce_to_basic(letter: str) -> str:
    """
    Function that reduces letters with special characters to its basic
    form. "unicodedata.cdecomposition" returns a string. It can be empty 
    (in case the letter is already a basic one: a, e, etc.), or it contains
    a code, in hexadecimal format. In that case, the code is returned as a 
    string, i.e., "ö" will return "006F 0308", where 006F corresponds to "o"
    and 0308 is the char "¨". So that, we just need to get that first part
    from the string."
    """
    letter_code: list[str] = []
    only_basic: str = ""
    decomposition = unicodedata.decomposition(letter)
    if letter == "ñ":
        return letter
    if decomposition == "":
        return letter
    else:
        letter_code = decomposition.split(" ")
        only_basic = "".join(letter_code[0])
        return chr(int(only_basic, 16))


def letter_was_guessed(sentence: str, letter: str, coded_phrase: str) -> str:
    """
    This function changes "_" if letter introduced by player exists in 
    the sentence that the gamer should guess.
    """
    coded_list: list[str] = list(coded_phrase)
    for i, alpha in enumerate(sentence):
        if reduce_to_basic(alpha).lower() == reduce_to_basic(letter).lower():
            coded_list[i] = alpha
    coded_phrase = "".join(coded_list)
    return coded_phrase


def how_many(letter: str, coded_fr: str) -> int:
    """
    Function in charge to calculate how many times a specific letter
    that was introduced appears in the phrase to guess. This number 
    is shown on the INFO panel.
    """
    count: int = 0
    for letra in coded_fr:
        if letra.lower() == letter.lower():
            count += 1
    return count


def plural_singular(num: int) -> str:
    """
    Function that keeps the gramatical accuracy of the word "vez/veces".
    1 vez / 2 veces. 
    """
    if num == 1:
        return "vez"
    else:
        return "veces"


def add_used_letters(letter: str, used_letters_: list[str]) -> list[str]:
    if letter.isalpha() and len(letter) == 1:
        used_letters_.append(letter)
    return used_letters_


def game_win(sentence) -> bool:
    win: bool = True
    sentence_list = list(sentence)
    if "_" in sentence_list:
        win = False
    return win


def main():
    letter: str = ""
    exit_game: str = "salir"
    ready_to_guess_full_phrase: str = "si"
    gallow_count: int = 0

    try:
        decoded_phrase = pick_phrase(sentences)
        coded_phrase = code_random_sentence(decoded_phrase)
        ui_hint(coded_phrase)
    except FileNotFoundError as _a:
        return ui_error()

    while True:
        letter = ui_ask("Escribe una letra")
        ready: str = ""

        add_used_letters(letter, used_letters)
        ui_letters(used_letters)

        if letter == exit_game:
            break

        if gallow_count >= 6:
            return ui_game_over()

        if letter.isalpha() and len(letter) == 1:
            if check_letter(letter, decoded_phrase):
                coded_phrase = letter_was_guessed(
                    decoded_phrase, letter, coded_phrase)
                ui_hint(coded_phrase)
                ui_show_info(
                    f"Enhorabuena, la letra \"{letter}\" sí está en la frase! "
                    f"Aparece: {how_many(letter, coded_phrase)} "
                    f"{plural_singular(how_many(letter, coded_phrase))}. "
                    f"Si estás listo para adivinar, escribe \"si\"!"
                )

                if game_win(coded_phrase):
                    return ui_win()

                ready = input("Si sabes escribe si, y si no, no: ")

                if ready.lower() == ready_to_guess_full_phrase:
                    try_full_phrase = input("Escribe toda la frase: ")

                    if try_full_phrase.lower() == decoded_phrase.lower():
                        return ui_win()
                    else:
                        gallow_count += 1
                        ui_gallow(gallow_count)
                        ui_show_info(
                            f"La frase \"{try_full_phrase}\" no es correcta :("
                            f" Puedes seguir intentando de letra en letra."
                        )

            else:
                gallow_count += 1
                ui_gallow(gallow_count)
                ui_show_info(
                    f"La letra \"{letter}\" no se encuentra en la frase :("
                    f"Prueba con otra!")

        else:
            print("Debes introducir una sola letra.")


if __name__ == "__main__":
    main()
