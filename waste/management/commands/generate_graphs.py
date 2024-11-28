from django.core.management.base import BaseCommand
from waste.workfiles.Generator import Generator


class Command(BaseCommand):
    help = "Генерация графов разных типов"

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['full', 'partial'],
            default='full',
            help="Тип графа для генерации: 'full' (полный), 'partial' (частичный)",
        )

    def handle(self, *args, **options):
        graph_type = options['type']

        if graph_type == 'full':
            Generator.generate_fully_graphs()
        elif graph_type == 'partial':
            Generator.generate_partially_graphs()
        else:
            self.stdout.write(self.style.ERROR(f"Неизвестный тип графа: {graph_type}"))