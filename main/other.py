from allauth.account.adapter import DefaultAccountAdapter


class AuthAdaptor(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # Disabling emails for now as my custom script sends the email to new members
        pass