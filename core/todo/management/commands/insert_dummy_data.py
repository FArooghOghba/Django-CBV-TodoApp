from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

from todo.models import Task


User = get_user_model()


class Command(BaseCommand):
    help = "Inserting dummy data for tasks."

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(),
            username=self.fake.user_name(),
            password='far121269'
        )
        user.is_verified = True
        user.save()

        for _ in range(5):
            Task.objects.create(
                user=user,
                title=self.fake.text(max_nb_chars=20),
                descriptions=self.fake.paragraph(nb_sentences=5),
                complete=self.fake.boolean(chance_of_getting_true=65)
            )