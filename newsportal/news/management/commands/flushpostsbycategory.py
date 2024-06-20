from django.core.management.base import BaseCommand, CommandError

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда удаляет все посты с заданной категории'
    missing_args_message = 'Недостаточно аргументов!'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить новости в категории {options["category"]}? да/нет')

        if answer != 'да':
            self.stdout.write('Действие отменено')
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Вы успешно удалили все новости из категгории {options["category"]}'))
        except Exception as e:
            self.stdout.write(e)
