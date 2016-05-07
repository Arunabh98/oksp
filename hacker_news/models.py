from django.db import models

<<<<<<< HEAD

class New(models.Model):
=======
class News(models.Model):
>>>>>>> 125bce7... First commit hacker-news
    '''
    News: Model class which holds all the shared links
    '''

    title = models.CharField(max_length=300)
<<<<<<< HEAD
    post_date = models.DateTimeField(auto_now = False, auto_now_add = True)
    description = models.TextField()
    link = models.URLField(max_length=200)
    upvotes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class comment(models.Model):
    comment_link = models.ForeignKey('self', blank=True, null=True)
    text = models.TextField()
    link = models.ForeignKey(New)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.text
=======
    link = models.URLField
    comments = models.IntegerField
    upvotes = models.IntegerField
>>>>>>> 125bce7... First commit hacker-news
