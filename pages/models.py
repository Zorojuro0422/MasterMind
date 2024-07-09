from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Accounts(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'accounts'

class Flashcard(models.Model):
    title = models.CharField(max_length=500, primary_key=True)
    user = models.ForeignKey('Accounts', on_delete=models.CASCADE)
    groups = models.ManyToManyField('Group', through='SharedFlashcard')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'flashcard'


class CreateFlashcard(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)  # Provide a default user ID
    flashcard_identifier = models.CharField(max_length=50)  # Rename the field
    difinition = models.CharField(max_length=500)
    term = models.CharField(max_length=500)

    def __str__(self):
        return self.difinition

    class Meta:
        db_table = 'createflashcard'

@receiver(post_delete, sender=CreateFlashcard)
def delete_flashcard(sender, instance, **kwargs):
    # Check if the associated Flashcard has no more associated CreateFlashcards
    if not CreateFlashcard.objects.filter(flashcard=instance.flashcard).exists():
        instance.flashcard.delete()

class Notes(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    content = models.CharField(max_length=500, default='Empty Note')
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notes'

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_title = models.CharField(max_length=255)
    group_members = models.ManyToManyField('Accounts')
    flashcards = models.ManyToManyField('Flashcard', through='SharedFlashcard')
    notes = models.ManyToManyField('Notes', through='SharedNote')  # New field for shared notes

    def __str__(self):
        return self.group_title

    class Meta:
        db_table = 'groups'

class ChatMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} in {self.group.group_title}: {self.message}'

    class Meta:
        db_table = 'chat_messages'
        ordering = ('timestamp',)

class SharedFlashcard(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)


class CompilerSubmission(models.Model):
    code = models.TextField()
    result = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} - {self.submission_time}"
    
class SharedNote(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
