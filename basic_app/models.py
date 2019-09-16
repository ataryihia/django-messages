from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UseProfileInfo(models.Model):

    user = models.OneToOneField(User,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class MessagesInfo(models.Model):
    sender_msg = models.ForeignKey(User, null=True, related_name= 'sender_msg' , on_delete=models.CASCADE)
    reciver_msg = models.ForeignKey(User, null=True, related_name= 'reciver_msg' , on_delete=models.CASCADE)
    message_body = models.CharField(blank=True, null=True, max_length=225)
    subject = models.CharField(blank=True, null=True, max_length=225)
    #  options for status:
    # was readedn
    #
    status = models.CharField(blank=True, null=True, max_length=225)
    created_at = models.DateTimeField(auto_now=True)


    @property
    def get_special_combination_value(self):
        return '{}{}{}{}{}{}'.format(self.subject, self.message_body, self.created_at, self.status)

    def __str__(self):
        return self.subject
