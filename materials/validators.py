from rest_framework.serializers import ValidationError


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get('url')
        if url and not url.startswith("https://www.youtube.com/"):
            raise ValidationError("Видео может быть только с youtube.com")
