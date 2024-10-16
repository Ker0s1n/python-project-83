import validators


def validate(url):
    errors = {}
    if validators.url(url):
        errors["url_adress"] = "This is not URL!"
    if url.get("url_adress") is None:
        errors["url_adress"] = "URL не должен быть пустым"
    elif len(url["url_adress"]) >= 255:
        errors["url_adress"] = "URL должен быть короче 255 символов"
    return errors
