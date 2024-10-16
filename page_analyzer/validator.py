import validators


def validate(url):
    errors = {}
    if not validators.url(url["url"]):
        errors["url"] = "This is not URL!"
    if url.get("url") == '':
        errors["url"] = "URL не должен быть пустым"
    if len(url["url"]) >= 255:
        errors["url"] = "URL должен быть короче 255 символов"
    return errors
