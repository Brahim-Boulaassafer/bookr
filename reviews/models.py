from django.db import models
from django.contrib import auth

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=50,help_text="Publisher ")
    website = models.URLField(help_text="Publisher's website")
    email = models.EmailField(help_text="Publisher's Email")


    def __str__(self):
        return self.name
    

class Contributor(models.Model):
    first_names = models.CharField(max_length=50,help_text="Contributor's First Name")
    last_names = models.CharField(max_length=50,help_text="Contributor's Last Name")
    email = models.EmailField(help_text="Contributor's Email")



    def __str__(self):
        return f"{self.first_names} {self.last_names}"
    

class Book(models.Model):
    title = models.CharField(max_length=70,help_text="Book Title")
    publication_date = models.DateTimeField(verbose_name="Published on")
    isbn = models.CharField(max_length=30,help_text="Book Serie Number")
    publisher = models.ForeignKey(Publisher, on_delete= models.CASCADE)
    contributors = models.ManyToManyField(Contributor, through="BookContributor")



    def __str__(self):
        return self.title
    



class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR","Author"
        CO_AUTHOR = "CO_AUTHOR","Co-Author"
        EDITOR = "EDITOR","Editor"

    book = models.ForeignKey(Book, on_delete= models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete= models.CASCADE)
    role = models.CharField(verbose_name="The role this contributer had in the book.",choices=ContributionRole.choices,max_length=20)


    def __str__(self):
        return f"{self.book.title} - {self.contributor.last_names}"
    

class Review(models.Model):
    content = models.TextField(help_text="The Review text")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True,help_text="The date and time the reiew was created.")
    date_edited = models.DateTimeField(null=True,help_text="The date and time the review was ladt edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete= models.CASCADE,help_text="The book that has this review")


