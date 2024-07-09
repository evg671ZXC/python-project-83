import validators


def validate(url):
    errors = []
    if url is None:
        errors.append("Required input field")
    if not validators.url(url):
        errors.append("URL's entered incorrectly")
    if len(url) > 255:
        errors.append("URL's longer than 255 characters")
    return errors
