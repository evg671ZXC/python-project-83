import validators


def validate(url):
    errors = []
    if url == '':
        errors.append("Заполните это поле")
    if not validators.url(url):
        errors.append("Некорректный URL")
    if len(url) > 255:
        errors.append("URL превышает 255 символов")
    return errors
