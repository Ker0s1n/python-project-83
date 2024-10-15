def validate(url):
    errors = {}
    if url.get("name") is None:
        errors["name"] = "URL не должен быть пустым"
    elif len(url["name"]) >= 255:
        errors["name"] = "URL должен быть короче 255 символов"
    return errors
