import requests


def get_random_joke() -> str:
    response = requests.get("https://witzapi.de/api/joke")
    if response.status_code == "200":
        return response.json()[0]["text"]
    return ""


def remove_newlines(s: str) -> str:
    s.replace("\n", " ")
    while "  " in s:
        s = s.replace("  ", " ")


joke = get_random_joke()
print(joke)
print(remove_newlines(joke))
