from django.db import models
from authentification.models import MyUser as User

class Transactions(models.Model):
    operation = models.CharField(max_length=100)
    ref = models.CharField(max_length=255, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    user_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=False, blank=True)
    is_validated = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.operation} à {self.user_to.account_num}"
    
    def serialise(self):
        return {
            'id': self.id,
            'operation': self.operation,
            'ref': self.ref,
            'balance': self.balance,
            'created_at': self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            'user_from': self.user_from.serialise(),
            'user_to': self.user_to.serialise(),
            'user_from_str': f"{self.user_from.first_name} {self.user_from.last_name}",
            'user_to_str': f"{self.user_to.first_name} {self.user_to.last_name}",
        }