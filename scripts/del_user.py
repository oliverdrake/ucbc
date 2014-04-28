import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ucbc.settings.dev")

from allauth.account.models import EmailAddress
from allauth.utils import get_user_model


if __name__ == "__main__":
    get_user_model().objects.get(username="oliverdrake").delete()
    # EmailAddress.objects.get(email="admin@ucbc.org.nz").delete()
