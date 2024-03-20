import re


def detect_language(page):
    text = page.split('.wikipedia')
    if re.search('[a-z][a-z]', text[0][-2:]):
        return text[0][-2:]
    else:
        return 'none'


def lang_code(code):
    if code == 'zh':
        return 'Chinese'
    elif code == 'fr':
        return 'French'
    elif code == 'en':
        return 'English'
    elif code == 'ru':
        return 'Russian'
    elif code == 'de':
        return 'German'
    elif code == 'ja':
        return 'Japanese'
    elif code == 'es':
        return 'Spanish'
    else:
        return 'None'
