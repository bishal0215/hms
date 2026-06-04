from django.db import models  # type: ignore[reportMissingModuleSource]

class Table(models.Model):
    number = models.IntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number}"

