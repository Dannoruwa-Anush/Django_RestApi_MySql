from django.db import models

# Create your models here.
class Users(models.Model):
    # Define fields of the table "Users"
    id = models.AutoField(primary_key=True)  # Explicit primary key field
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
