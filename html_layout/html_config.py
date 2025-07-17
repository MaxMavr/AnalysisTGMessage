DEFAULT_COLOR: str = '#1A1A1A'
TRANSPARENT_COLOR: str = '#FFFFFF'

SENSIBLE_COLOR: str = '#f72585'
FORWARDED_COLOR: str = ''
PIN_COLOR: str = ''
VOICES_COLOR: str = '#7209b7'
VIDEOS_COLOR: str = '#480ca8'
PHONE_CALL_COLOR: str = ''
STICKERS_COLOR: str = '#3f37c9'

SENSIBLE_LIGHT_COLOR: str = SENSIBLE_COLOR + 'AA'
FORWARDED_LIGHT_COLOR: str = FORWARDED_COLOR + 'AA'
PIN_LIGHT_COLOR: str = PIN_COLOR + 'AA'
VOICES_LIGHT_COLOR: str = VOICES_COLOR + 'AA'
VIDEOS_LIGHT_COLOR: str = VIDEOS_COLOR + 'AA'
PHONE_CALL_LIGHT_COLOR: str = PHONE_CALL_COLOR + 'AA'
STICKERS_LIGHT_COLOR: str = STICKERS_COLOR + 'AA'

HTML_START: str = \
    '''<!DOCTYPE html>
    <html lang="ru-RU">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Анализ сообщений</title>
        <link rel="icon" type="image/png" sizes="16x16" href="https://web.telegram.org/k/assets/img/favicon-16x16.png?v=jw3mK7G9Ry">
        <link rel="stylesheet" type="text/css" href="style.css">
      </head>
    </head>
    <body>'''
HTML_END: str = '</main><script src="script.js"></script></body>'
