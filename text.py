import requests


def get_random_joke() -> str:
    response = requests.get("https://witzapi.de/api/joke")
    if response.status_code == "200":
        return response.json()[0]["text"]
    return ""


def remove_newlines(input_string: str) -> str:
    s = input_string[:]
    s.replace("\n", " ")
    while "  " in s:
        s.replace("  ", " ")
    return s


if __name__ == "__main__":
    joke = get_random_joke()
    print(joke)
    print(remove_newlines(joke))
