from django.db import models


class SubjectChoice(models.TextChoices):
    sport = 'SP', 'Sport'
    economy = 'EC', 'Economy'
    politics = 'PO', 'Politics'

class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=2, choices=SubjectChoice, default=SubjectChoice.sport)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='posts')


    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست'


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    body = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
    
    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ['-created_at']
    

class HxPost(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("published", "Published")]
    )
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title