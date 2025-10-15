from django.core.exceptions import ValidationError
import re

def validate_youtube_link(value):
    """
    Проверяет, что ссылка ведёт на YouTube.
    Разрешены форматы:
    - https://www.youtube.com/watch?v=...
    - https://youtube.com/watch?v=...
    - https://youtu.be/...
    """
    # Регулярное выражение для YouTube
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu\.be)'
        r'\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    if not re.match(youtube_regex, value):
        raise ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com или youtu.be).'
        )
