from django.db import models


class Floor(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)

    class Meta:
        ordering = ['level', 'name']

    def __str__(self):
        return f"{self.name} (Level {self.level})"


class Table(models.Model):
    STATUS_FREE = 'free'
    STATUS_OCCUPIED = 'occupied'
    STATUS_RESERVED = 'reserved'

    STATUS_CHOICES = [
        (STATUS_FREE, 'Free'),
        (STATUS_OCCUPIED, 'Occupied'),
        (STATUS_RESERVED, 'Reserved'),
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='tables')
    number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_FREE)

    class Meta:
        ordering = ['floor__level', 'number']

    @property
    def display_number(self):
        if self.number >= 100:
            return self.number
        return int(f"{self.floor.level}{self.number:02d}")

    def __str__(self):
        return f"Table {self.display_number}"
