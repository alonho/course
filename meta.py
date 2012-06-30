class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

guy = Person(name='bob', age='35')
print guy.age