from django.db import models


class Word(models.Model):
    word = models.TextField(help_text='Query word.')
    audio = models.TextField(help_text='Audio file.')
    label = models.TextField(help_text='Functional label.')
    sense = models.TextField(help_text='Senses of the query word.')
    ymd = models.DateTimeField(help_text='Entry creating date and time.', auto_now_add=True, blank=True)
    favorite = models.BooleanField(help_text='Add to favorite.', default=False)

