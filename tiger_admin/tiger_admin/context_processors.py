import models

def common(request):
    if request.user.is_authenticated():
        account = models.Account.objects.get(username__exact=request.user.username)
        is_admin = account.account_type == models.Account.ACCOUNT_TYPE_ADMIN
        vals = {
            "is_admin": is_admin,
            "is_superuser": request.user.is_superuser
        }
        return vals
    else:
        return {}