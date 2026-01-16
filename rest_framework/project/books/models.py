from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=150)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="books"
    )
    publication_date = models.DateField(editable=False)
    pages = models.IntegerField()

    def __str__(self) -> str:
        return str(self.title)
