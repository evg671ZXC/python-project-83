import validators


def validate(url):
    errors = []
    if url == '':
        errors.append("Заполните это поле")
    if len(url) > 255:
        errors.append("URL превышает 255 символов")
    if not validators.url(url):
        errors.append("Некорректный URL")
    return errors
