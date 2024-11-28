from django.core.management.base import BaseCommand
from waste.workfiles.Generator import Generator


class Command(BaseCommand):
    help = "Генерация графов разных типов, в зависимости от того, что мы хотим проверить"

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['base', 'spec', 'intersection', 'error'],
            default='base',
            help="Тип графа для генерации: 'base' (Стандартный вариант из примера задания),"
                 " 'spec' (Специальный граф(Полный обхода всех хранилищ, \
           проверка функции возврата к организации в случае тупика, производимое кол-во отходов == ёмкостям хранилищ)),"
                 "'intersection'(Полный обход хранилищ, кол-во отходов == ёмкостям хранилищ,"
                 " у организаций есть общие пути)"
                 "'error'(Полный обход хранилищ, кол-во отходов > сумма ёмкости хранилищ"
                 "(причём для каждой организации))",
        )

    def handle(self, *args, **options):
        graph_type = options['type']

        if graph_type == 'base':
            Generator.generate_test_graph()
        elif graph_type == 'spec':
            Generator.generate_specific_graph()
        elif graph_type == 'intersection':
            Generator.generate_graph_with_intersections()
        elif graph_type == 'error':
            Generator.generate_error_graph()
        else:
            self.stdout.write(self.style.ERROR(f"Неизвестный тип графа: {graph_type}"))