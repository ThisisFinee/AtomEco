from django.urls import get_resolver, URLPattern, URLResolver
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Посмотреть все urls"

    def handle(self, *args, **options):
        def extract_urls(patterns, prefix=""):
            urls = []
            for pattern in patterns:
                if isinstance(pattern, URLPattern):  # Это одиночный маршрут
                    urls.append(f"{prefix}{pattern.pattern}")
                elif isinstance(pattern, URLResolver):  # Это include()
                    nested_prefix = f"{prefix}{pattern.pattern}/"
                    urls.extend(extract_urls(pattern.url_patterns, nested_prefix))
            return urls

        resolver = get_resolver()
        all_urls = extract_urls(resolver.url_patterns)
        self.stdout.write("\n".join(all_urls))

