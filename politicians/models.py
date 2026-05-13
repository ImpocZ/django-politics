from django.db import models


class Politician(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    title = models.CharField(max_length=50, blank=True, null=True)
    photo = models.BinaryField(blank=True, null=True)
    photo_file = models.ImageField(upload_to='photos/politicians/', blank=True, null=True)
    age = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'politician'

    def __str__(self):
        return f"{self.name} {self.surname}"


class Party(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    founding = models.IntegerField()
    leader = models.CharField(max_length=75)
    photo = models.BinaryField(blank=True, null=True)
    photo_file = models.ImageField(upload_to='photos/parties/', blank=True, null=True)

    class Meta:
        db_table = 'party'

    def __str__(self):
        return self.name


class Office(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'office'

    def __str__(self):
        return self.name


class Government(models.Model):
    id = models.IntegerField(primary_key=True)
    in_function = models.DateField()
    prime_minister = models.CharField(max_length=50)

    class Meta:
        db_table = 'government'

    def __str__(self):
        return f"Government {self.id} - {self.in_function}"


class GovernmentOfficial(models.Model):
    id = models.AutoField(primary_key=True)
    government = models.ForeignKey(Government, on_delete=models.CASCADE, db_column='id_government')
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, db_column='id_politician')
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_party')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, db_column='id_office')
    ROLE_CHOICES = [
        ('Minister', 'Minister'),
        ('Speaker of the house', 'Speaker of the house'),
        ('Deputy', 'Deputy'),
        ('Deputy speaker', 'Deputy speaker'),
        ('Prime minister', 'Prime minister'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)
    start_of_term = models.DateField()
    end_of_term = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'government_official'
        unique_together = (('politician', 'government', 'office'),)


class GovernmentParty(models.Model):
    id = models.AutoField(primary_key=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='id_party')
    government = models.ForeignKey(Government, on_delete=models.CASCADE, db_column='id_government')

    class Meta:
        db_table = 'government_party'
        unique_together = (('party', 'government'),)


class PoliticsParty(models.Model):
    id = models.AutoField(primary_key=True)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, db_column='id_politician')
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='id_party')
    start_of_membership = models.DateField()
    end_of_membership = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'politics_party'
        unique_together = (('politician', 'party'),)
