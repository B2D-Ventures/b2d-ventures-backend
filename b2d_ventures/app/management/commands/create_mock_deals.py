import os
from datetime import timedelta
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.utils import timezone

from b2d_ventures.app.models import Startup, Deal


class Command(BaseCommand):
    help = "Creates mock deals for a startup"

    def handle(self, *args, **options):
        def create_placeholder_image(folder, filename):
            with open(
                f"/Users/krittinsetdhavanich/Downloads/b2d-ventures-backend/contentMockup/{folder}/{filename}",
                "rb",
            ) as f:
                content = ContentFile(f.read())
            path = os.path.join("contentMockup", folder, filename)
            full_path = default_storage.save(path, content)
            return full_path

        def create_placeholder_pdf(folder, filename):
            with open(
                f"/Users/krittinsetdhavanich/Downloads/b2d-ventures-backend/contentMockup/{folder}/{filename}",
                "rb",
            ) as f:
                content = ContentFile(f.read())
            path = os.path.join("contentMockup", folder, filename)
            full_path = default_storage.save(path, content)
            return full_path

        def create_mock_deals(startup_id):
            startup = Startup.objects.get(id=startup_id)

            deals = []

            # Deal 1: Tech Startup
            deal1 = Deal.objects.create(
                startup=startup,
                name="NeurAI Series A",
                description="Revolutionizing human-computer interaction with direct neural interfaces",
                content="NeurAI is developing cutting-edge neural interface technology that allows direct communication between the human brain and computers. Our technology has applications in healthcare, gaming, and productivity tools.",
                image_background=create_placeholder_image(
                    "NeurAI", "neurai_background.jpeg"
                ),
                image_logo=create_placeholder_image("NeurAI", "neurai_logo.png"),
                image_content=create_placeholder_image("NeurAI", "neurai_content.jpeg"),
                dataroom=create_placeholder_pdf("NeurAI", "neurai_dataroom.pdf"),
                allocation=Decimal("5000000.00"),
                price_per_unit=Decimal("100.00"),
                minimum_investment=Decimal("10000.00"),
                type="Equity",
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=90),
            )
            deals.append(deal1)

            # Deal 2: Green Energy Startup
            deal2 = Deal.objects.create(
                startup=startup,
                name="SolarFlare Seed Round",
                description="Efficient and affordable solar solutions for residential use",
                content="SolarFlare is developing a new generation of solar panels that are 50% more efficient and 30% cheaper than current market leaders. Our technology will make solar energy accessible to millions of homeowners.",
                image_background=create_placeholder_image(
                    "SolarFlare", "solarflare_background.png"
                ),
                image_logo=create_placeholder_image(
                    "SolarFlare", "solarflare_logo.png"
                ),
                image_content=create_placeholder_image(
                    "SolarFlare", "solarflare_background.png"
                ),
                dataroom=create_placeholder_pdf(
                    "SolarFlare", "solarflare_dataroom.pdf"
                ),
                allocation=Decimal("2000000.00"),
                price_per_unit=Decimal("50.00"),
                minimum_investment=Decimal("5000.00"),
                type="Convertible Note",
                start_date=timezone.now() - timedelta(days=30),
                end_date=timezone.now() + timedelta(days=60),
            )
            deals.append(deal2)

            # Deal 3: Biotech Startup
            deal3 = Deal.objects.create(
                startup=startup,
                name="GeneCure Series B",
                description="Advancing personalized medicine through innovative gene therapies",
                content="GeneCure is at the forefront of personalized medicine, developing gene therapies tailored to individual genetic profiles. Our treatments show promise in addressing previously incurable genetic disorders.",
                image_background=create_placeholder_image(
                    "GeneCure", "genecure_background.jpg"
                ),
                image_logo=create_placeholder_image("GeneCure", "genecure_logo.jpg"),
                image_content=create_placeholder_image(
                    "GeneCure", "genecure_background.jpg"
                ),
                dataroom=create_placeholder_pdf("GeneCure", "genecure_dataroom.pdf"),
                allocation=Decimal("20000000.00"),
                price_per_unit=Decimal("500.00"),
                minimum_investment=Decimal("50000.00"),
                type="Equity",
                start_date=timezone.now() - timedelta(days=60),
                end_date=timezone.now() + timedelta(days=30),
            )
            deals.append(deal3)

            # Deal 4: Fintech Startup
            deal4 = Deal.objects.create(
                startup=startup,
                name="CryptoBank ICO",
                description="Bringing traditional banking services to the blockchain",
                content="CryptoBank is building a decentralized banking platform that offers traditional banking services using blockchain technology. Our platform will provide secure, transparent, and accessible financial services to anyone with an internet connection.",
                image_background=create_placeholder_image(
                    "CryptoBank", "cryptobank_background.jpeg"
                ),
                image_logo=create_placeholder_image(
                    "CryptoBank", "cryptobank_logo.jpeg"
                ),
                image_content=create_placeholder_image(
                    "CryptoBank", "cryptobank_content.jpeg"
                ),
                dataroom=create_placeholder_pdf(
                    "CryptoBank", "cryptobank_dataroom.pdf"
                ),
                allocation=Decimal("10000000.00"),
                price_per_unit=Decimal("1.00"),
                minimum_investment=Decimal("1000.00"),
                type="Token Sale",
                start_date=timezone.now() - timedelta(days=15),
                end_date=timezone.now() + timedelta(days=15),
            )
            deals.append(deal4)

            # Deal 5: AgTech Startup
            deal5 = Deal.objects.create(
                startup=startup,
                name="VertiFarm Series A",
                description="Revolutionizing urban agriculture with AI-powered vertical farms",
                content="VertiFarm is developing AI-controlled vertical farming systems that can produce 100 times more food per square foot than traditional farming. Our technology enables fresh, local produce to be grown year-round in any urban environment.",
                image_background=create_placeholder_image(
                    "VertiFarm", "vertifarm_background.png"
                ),
                image_logo=create_placeholder_image("VertiFarm", "vertifarm_logo.png"),
                image_content=create_placeholder_image(
                    "VertiFarm", "vertifarm_background.png"
                ),
                dataroom=create_placeholder_pdf("VertiFarm", "vertifarm_dataroom.pdf"),
                allocation=Decimal("8000000.00"),
                price_per_unit=Decimal("200.00"),
                minimum_investment=Decimal("20000.00"),
                type="Equity",
                start_date=timezone.now() - timedelta(days=45),
                end_date=timezone.now() + timedelta(days=45),
            )
            deals.append(deal5)

            return deals

        startup_id = "0d3b7d0e-9e10-4254-b94d-30cfbab66ed8"
        mock_deals = create_mock_deals(startup_id)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(mock_deals)} mock deals for startup with ID: {startup_id}"
            )
        )
