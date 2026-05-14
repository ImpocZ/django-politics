from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


alphabetic_validator = RegexValidator(
    regex=r'^[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]*$',
    message='This field must start with a capital letter and contain only letters.',
)


def validate_letters_only(value):
    normalized_value = value.replace(' ', '')
    if not normalized_value.isalpha():
        raise ValidationError('This field can contain only letters.')


def validate_founding_year(value):
    current_year = date.today().year
    if value < 1880 or value > current_year:
        raise ValidationError(f'The founding year must be between 1880 and {current_year}.')


class Politician(models.Model):
    name = models.CharField(max_length=50, validators=[alphabetic_validator])
    surname = models.CharField(max_length=50, validators=[alphabetic_validator])
    title = models.CharField(max_length=50, blank=True, null=True)
    photo = models.BinaryField(blank=True, null=True)
    photo_file = models.ImageField(upload_to='photos/politicians/', blank=True, null=True)
    age = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(21), MaxValueValidator(100)])

    class Meta:
        db_table = 'politician'
        verbose_name = "politik"
        verbose_name_plural = "politici"
    def __str__(self):
        return f"{self.name} {self.surname}"


class Party(models.Model):
    name = models.CharField(max_length=50)
    founding = models.IntegerField(validators=[validate_founding_year])
    leader = models.CharField(max_length=75)
    photo = models.BinaryField(blank=True, null=True)
    photo_file = models.ImageField(upload_to='photos/parties/', blank=True, null=True)

    class Meta:
        db_table = 'party'
        verbose_name = 'strana'
        verbose_name_plural = 'strany'

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=200, validators=[validate_letters_only])
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'office'
        verbose_name = 'funkce'
        verbose_name_plural = 'funkce'
    def __str__(self):
        return self.name


class Government(models.Model):
    in_function = models.DateField()
    prime_minister = models.CharField(max_length=50, validators=[validate_letters_only])

    class Meta:
        db_table = 'government'
        verbose_name = 'vláda'
        verbose_name_plural = 'vlády'
    def __str__(self):
        return f"Government {self.id} - {self.in_function}"


class GovernmentOfficial(models.Model):
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
        verbose_name = "vládní funkce"
        verbose_name_plural = "vládní funkce"
        unique_together = (('politician', 'government', 'office'),)


class GovernmentParty(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='id_party')
    government = models.ForeignKey(Government, on_delete=models.CASCADE, db_column='id_government')

    class Meta:
        db_table = 'government_party'
        verbose_name = "vládnoucí strana"
        verbose_name_plural = "vládnoucí strany"
        unique_together = (('party', 'government'),)


class PoliticsParty(models.Model):
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE, db_column='id_politician')
    party = models.ForeignKey(Party, on_delete=models.CASCADE, db_column='id_party')
    start_of_membership = models.DateField()
    end_of_membership = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'politics_party'
        verbose_name = "strana politika"
        verbose_name_plural = "strany politiků"
        unique_together = (('politician', 'party'),)
