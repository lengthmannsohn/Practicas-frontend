from django.core.management.base import BaseCommand
from core.models import Professional, Client
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Crea datos ficticios: 10 profesionales y 10 clientes"

    def handle(self, *args, **options):
        if Professional.objects.exists() or Client.objects.exists():
            self.stdout.write(self.style.WARNING("Ya hay datos, no hago nada."))
            return

        barrios = [
            (40.4168, -3.7038),  # Centro
            (40.4300, -3.6870),  # Salamanca
            (40.4520, -3.6920),  # Chamartín
            (40.4480, -3.7030),  # Tetuán
            (40.4030, -3.7000),  # Arganzuela
        ]

        plans = ['free', 'standard', 'premium']

        nombres = [
            'Luna', 'Eva', 'Claudia', 'Marta', 'Sofía',
            'Noa', 'Aitana', 'Vega', 'Irene', 'Paula'
        ]

        self.stdout.write("Creando profesionales...")
        for i, nombre in enumerate(nombres):
            lat_base, lng_base = random.choice(barrios)
            lat = lat_base + random.uniform(-0.01, 0.01)
            lng = lng_base + random.uniform(-0.01, 0.01)
            plan = random.choice(plans)
            price_from = random.choice([80, 100, 120, 150])
            price_to = price_from + random.choice([20, 40, 60])

            Professional.objects.create(
                name=f"{nombre} Real",
                alias=nombre,
                phone=f"+34 600 00 {i:03d}",
                bio=f"{nombre} es una acompañante discreta y elegante en Madrid. "
                    "Este es un texto ficticio para la demo de la plataforma.",
                price_from=price_from,
                price_to=price_to,
                lat=lat,
                lng=lng,
                plan=plan,
                is_active=True,
                created_at=timezone.now(),
            )

        self.stdout.write("Creando clientes...")
        for i in range(1, 11):
            Client.objects.create(
                name=f"Cliente {i}",
                email=f"cliente{i}@example.com",
                created_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados correctamente."))
