import os
from datetime import timedelta
from decimal import Decimal

from django.core.files.base import ContentFile
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
from django.core.management.base import BaseCommand
from django.utils import timezone

from b2d_ventures.app.models import Startup, Deal


class Command(BaseCommand):
    help = "Creates mock deals for a startup"

    def handle(self, *args, **options):
        media_storage = MediaCloudinaryStorage()
        raw_storage = RawMediaCloudinaryStorage()

        def upload_to_cloudinary(folder, filename, file_path, is_raw=False):
            with open(file_path, "rb") as f:
                content = ContentFile(f.read())

            path = f"{folder}/{filename}"
            return (
                raw_storage.save(path, content)
                if is_raw
                else media_storage.save(path, content)
            )

        def create_placeholder_file(folder, filename):
            local_path = f"/Users/krittinsetdhavanich/Downloads/b2d-ventures-backend/contentMockup/{folder}/{filename}"
            is_raw = filename.lower().endswith(".pdf")
            return upload_to_cloudinary(folder, filename, local_path, is_raw=is_raw)

        def create_mock_deals(startup_id):
            startup = Startup.objects.get(id=startup_id)

            deals = []

            deal1 = Deal.objects.create(
                startup=startup,
                name="GreenSpark Series B",
                description="Leading the transition to renewable energy sources",
                content=(
                    "GreenSpark is a transformative force in the renewable energy sector, dedicated to revolutionizing the way communities produce "
                    "and consume energy. Our flagship product line includes ultra-efficient solar panels that utilize quantum dot technology to achieve "
                    "over 95% energy conversion efficiency, alongside compact wind turbines specifically designed for urban landscapes. GreenSpark’s innovative "
                    "approach also extends to hydroelectric systems optimized for low-flow rivers, enabling renewable energy generation in previously untapped regions. "
                    "Beyond our product offerings, GreenSpark actively collaborates with global governments and NGOs to implement clean energy initiatives tailored to developing nations. "
                    "By integrating AI and IoT solutions, our smart grids ensure optimal distribution of energy, minimizing losses and enhancing reliability. "
                    "Our commitment to sustainability is evident in our closed-loop manufacturing processes, which prioritize recycled materials and renewable energy in production. "
                    "With GreenSpark, the vision of a carbon-neutral future is not only possible but within reach. \n\n"
                    "Expanding on our innovations, GreenSpark is actively developing community-level microgrid solutions to bring affordable energy to underserved regions. "
                    "These systems empower communities to generate, store, and share power autonomously, fostering energy independence. Our cutting-edge research in energy storage "
                    "has also yielded next-generation batteries with extended lifespans and unparalleled performance, further enhancing the utility of renewable energy sources. "
                    "GreenSpark’s holistic approach to clean energy incorporates educational programs aimed at raising awareness about sustainability and training future generations "
                    "in renewable energy technologies. By pushing the boundaries of green innovation and forging strategic partnerships, GreenSpark continues to lead the charge toward "
                    "a sustainable and equitable energy future."
                ),
                image_background=create_placeholder_file("GreenSpark", "greenspark_background.png"),
                image_logo=create_placeholder_file("GreenSpark", "greenspark_logo.png"),
                image_content=create_placeholder_file("GreenSpark", "greenspark_content.png"),
                dataroom=create_placeholder_file("GreenSpark", "greenspark_dataroom.pdf"),
                target_amount=Decimal("10000000.00"),
                price_per_unit=Decimal("50.00"),
                minimum_investment=Decimal("5000.00"),
                type="Renewable Energy",
                start_date=timezone.now() - timedelta(days=20),
                end_date=timezone.now() + timedelta(days=90),
                status="approved"
            )
            deals.append(deal1)

            deal2 = Deal.objects.create(
                startup=startup,
                name="LifeGene Series A",
                description="Pioneering the future of personalized medicine",
                content=(
                    "LifeGene is redefining the future of healthcare with a revolutionary platform that enables precise genetic editing to treat and potentially cure a wide range of conditions. "
                    "Our flagship gene therapy, GenomicX™, targets inherited disorders like sickle cell anemia and cystic fibrosis, delivering life-changing results. Beyond medical applications, "
                    "LifeGene is pioneering new frontiers in agriculture by engineering drought-resistant crops that can thrive in extreme climates, addressing food security on a global scale. "
                    "Partnering with leading pharmaceutical companies, LifeGene is accelerating the development of personalized treatments that consider an individual's unique genetic profile. "
                    "LifeGene’s ethical framework ensures all advancements are implemented with transparency and inclusivity, making cutting-edge treatments accessible worldwide. "
                    "With an extensive pipeline of therapies in development and a robust intellectual property portfolio, LifeGene is set to dominate the biotechnology landscape for decades to come. \n\n"
                    "Furthermore, LifeGene is investing heavily in precision medicine technologies that utilize AI to analyze genomic and epigenomic data, enabling real-time adaptation of treatment strategies. "
                    "Our state-of-the-art labs leverage CRISPR-based tools to pioneer innovations in cellular regeneration and immunity enhancement, offering new hope for cancer and autoimmune disease patients. "
                    "In the agricultural sector, LifeGene is leading efforts to combat the challenges of climate change by developing crops that are not only drought-resistant but also more nutritious and higher-yielding. "
                    "We are also advancing eco-friendly pest-resistant plant strains, reducing dependency on chemical pesticides. By continuously pushing the envelope of biotechnological advancement, "
                    "LifeGene is committed to transforming lives and ecosystems globally."
                ),
                image_background=create_placeholder_file("LifeGene", "lifegene_background.jpeg"),
                image_logo=create_placeholder_file("LifeGene", "lifegene_logo.png"),
                image_content=create_placeholder_file("LifeGene", "lifegene_content.jpg"),
                dataroom=create_placeholder_file("LifeGene", "lifegene_dataroom.pdf"),
                target_amount=Decimal("20000000.00"),
                price_per_unit=Decimal("200.00"),
                minimum_investment=Decimal("20000.00"),
                type="Biotechnology",
                start_date=timezone.now() - timedelta(days=45),
                end_date=timezone.now() + timedelta(days=45),
                status="approved"
            )
            deals.append(deal2)

            deal3 = Deal.objects.create(
                startup=startup,
                name="BrainLink Seed Round",
                description="Creating AI solutions to augment human intelligence",
                content=(
                    "BrainLink is revolutionizing artificial intelligence by creating solutions that augment human capabilities and transform industries. "
                    "CognitiveCore™, our flagship AI platform, uses advanced machine learning algorithms to analyze and interpret massive datasets in real-time, "
                    "providing actionable insights for businesses. In healthcare, BrainLink assists doctors in identifying complex patterns in medical imaging, "
                    "enhancing diagnostic accuracy. In finance, it forecasts market trends with unparalleled precision, empowering investors to make informed decisions. "
                    "BrainLink also prioritizes ethical AI development, ensuring fairness, accountability, and transparency in all its applications. \n\n"
                    "Our educational initiatives aim to close the AI skills gap, providing training resources to empower individuals and businesses to harness the potential of AI. "
                    "Beyond commercial applications, BrainLink is driving advancements in AI-assisted creative industries, enabling the generation of innovative art, music, and design. "
                    "We also support urban planning efforts with AI solutions that model sustainable cities, optimize transportation, and enhance energy distribution. "
                    "Through strategic collaborations with universities and research institutions, BrainLink is shaping the next generation of AI researchers and practitioners. "
                    "As we continue to push the boundaries of what AI can achieve, BrainLink remains committed to creating technology that enhances lives and drives global progress."
                ),
                image_background=create_placeholder_file("BrainLink", "brainlink_background.jpeg"),
                image_logo=create_placeholder_file("BrainLink", "brainlink_logo.png"),
                image_content=create_placeholder_file("BrainLink", "brainlink_content.png"),
                dataroom=create_placeholder_file("BrainLink", "brainlink_dataroom.pdf"),
                target_amount=Decimal("5000000.00"),
                price_per_unit=Decimal("100.00"),
                minimum_investment=Decimal("10000.00"),
                type="Artificial Intelligence",
                start_date=timezone.now() - timedelta(days=10),
                end_date=timezone.now() + timedelta(days=70),
                status="approved"
            )
            deals.append(deal3)

            deal4 = Deal.objects.create(
                startup=startup,
                name="EcoThread Bridge Round",
                description="AI-powered sustainable fashion manufacturing",
                content=(
                    "EcoThread is at the forefront of sustainable fashion, leveraging cutting-edge AI and advanced manufacturing techniques to create eco-friendly apparel "
                    "that minimizes environmental impact. Our AI-driven design platform optimizes fabric cutting patterns, reducing waste by over 70%. EcoThread exclusively uses "
                    "sustainable materials such as organic cotton, bamboo fibers, and recycled textiles, ensuring every garment is as environmentally friendly as it is stylish. "
                    "In addition, our production facilities operate on renewable energy, further reducing our carbon footprint. \n\n"
                    "EcoThread’s circular economy initiatives include a garment recycling program where customers can return old clothing to be transformed into new products, "
                    "closing the loop on fashion waste. Beyond manufacturing, EcoThread’s AI-based consumer insights platform empowers brands to predict trends and optimize inventory, "
                    "minimizing overproduction and unsold stock. We are also working on next-generation fabrics infused with nanotechnology for enhanced durability and performance. "
                    "Our collaboration with global fashion houses and independent designers underscores our commitment to bringing sustainability into mainstream fashion, "
                    "reshaping the industry into a force for environmental and social good."
                ),
                image_background=create_placeholder_file("EcoThread", "ecothread_background.jpeg"),
                image_logo=create_placeholder_file("EcoThread", "ecothread_logo.png"),
                image_content=create_placeholder_file("EcoThread", "ecothread_content.png"),
                dataroom=create_placeholder_file("EcoThread", "ecothread_dataroom.pdf"),
                target_amount=Decimal("4000000.00"),
                price_per_unit=Decimal("50.00"),
                minimum_investment=Decimal("10000.00"),
                type="Sustainable Fashion",
                start_date=timezone.now() - timedelta(days=15),
                end_date=timezone.now() + timedelta(days=45),
                status="approved"
            )
            deals.append(deal4)

            deal5 = Deal.objects.create(
                startup=startup,
                name="OrbitX Series B",
                description="Democratizing satellite launch services",
                content=(
                    "OrbitX is transforming space exploration by making satellite launch services more accessible and affordable than ever before. "
                    "Our reusable micro-satellite launch vehicles use cutting-edge propulsion systems that significantly reduce costs while maintaining unmatched reliability. "
                    "OrbitX's modular satellite components allow customers to customize their payloads with ease, making space accessible to startups, academic institutions, and smaller nations. "
                    "Our in-orbit refueling technology is a game-changer, enabling satellites to operate longer and reduce the accumulation of space debris. \n\n"
                    "In addition to satellite launches, OrbitX is pioneering space sustainability through satellite recycling and advanced orbital infrastructure development. "
                    "Our modular spacecraft components are designed to be easily upgraded or repaired in orbit, minimizing waste and extending mission lifespans. "
                    "We are also developing next-generation propulsion systems that leverage clean energy sources, reducing environmental impact even further. "
                    "OrbitX's vision includes establishing orbital repair and refueling stations, laying the groundwork for interplanetary missions. By collaborating with governmental and private stakeholders, "
                    "we are building a robust ecosystem to democratize access to space and drive humanity's expansion into the cosmos."
                ),
                image_background=create_placeholder_file("OrbitX", "orbitx_background.png"),
                image_logo=create_placeholder_file("OrbitX", "orbitx_logo.png"),
                image_content=create_placeholder_file("OrbitX", "orbitx_content.png"),
                dataroom=create_placeholder_file("OrbitX", "orbitx_dataroom.pdf"),
                target_amount=Decimal("25000000.00"),
                price_per_unit=Decimal("1000.00"),
                minimum_investment=Decimal("100000.00"),
                type="Space Exploration",
                start_date=timezone.now() - timedelta(days=20),
                end_date=timezone.now() + timedelta(days=70),
                status="approved"
            )
            deals.append(deal5)

            deal6 = Deal.objects.create(
                startup=startup,
                name="MediMind Pre-Series A",
                description="AI-powered medical diagnosis and treatment planning",
                content=(
                    "MediMind leverages advanced AI algorithms to assist healthcare providers in diagnosis and treatment planning. Our system analyzes medical imaging, patient history, and latest research "
                    "to provide accurate diagnostic suggestions and personalized treatment plans. MediMind’s algorithms are trained on diverse datasets, ensuring culturally and demographically inclusive medical insights. "
                    "Our technology reduces diagnostic errors, shortens hospital stays, and enhances patient outcomes. \n\n"
                    "Beyond diagnostics, MediMind is pioneering AI applications in drug discovery, accelerating the identification of potential therapeutic compounds. "
                    "We also integrate wearable health devices to provide real-time monitoring and predictive alerts for chronic conditions, enabling proactive healthcare. "
                    "Through strategic collaborations with hospitals and research institutions, MediMind is fostering a global network of knowledge-sharing to improve medical outcomes worldwide. "
                    "As healthcare challenges grow more complex, MediMind is dedicated to empowering providers with the tools they need to deliver exceptional care."
                ),
                image_background=create_placeholder_file("MediMind", "medimind_background.png"),
                image_logo=create_placeholder_file("MediMind", "medimind_logo.png"),
                image_content=create_placeholder_file("MediMind", "medimind_content.png"),
                dataroom=create_placeholder_file("MediMind", "medimind_dataroom.pdf"),
                target_amount=Decimal("3000000.00"),
                price_per_unit=Decimal("75.00"),
                minimum_investment=Decimal("15000.00"),
                type="Healthcare",
                start_date=timezone.now() - timedelta(days=10),
                end_date=timezone.now() + timedelta(days=80),
                status="approved"
            )
            deals.append(deal6)

            deal7 = Deal.objects.create(
                startup=startup,
                name="LearnVerse Seed Round",
                description="Virtual reality education platform",
                content=(
                    "LearnVerse creates immersive VR educational experiences that make learning engaging and effective. Our platform covers K-12 curriculum with interactive 3D models "
                    "and virtual laboratories. Students can explore complex scientific phenomena, historical events, and mathematical concepts in a hands-on, virtual environment, "
                    "bridging the gap between theory and practice. LearnVerse’s adaptive learning algorithms personalize educational experiences to cater to individual learning styles "
                    "and speeds, ensuring maximum retention and engagement. \n\n"
                    "In addition to K-12 education, LearnVerse is expanding its offerings to include professional training programs, enabling workers in industries such as healthcare, engineering, "
                    "and manufacturing to upskill through realistic simulations. By collaborating with educators and institutions worldwide, LearnVerse aims to make cutting-edge educational resources "
                    "accessible in even the most underserved regions. With features such as multilingual support and low-bandwidth optimization, our platform is built to overcome barriers to learning. "
                    "As we continue to innovate, LearnVerse is setting the standard for the future of education through the power of virtual reality."
                ),
                image_background=create_placeholder_file("LearnVerse", "learnverse_background.jpg"),
                image_logo=create_placeholder_file("LearnVerse", "learnverse_logo.png"),
                image_content=create_placeholder_file("LearnVerse", "learnverse_content.jpg"),
                dataroom=create_placeholder_file("LearnVerse", "learnverse_dataroom.pdf"),
                target_amount=Decimal("1500000.00"),
                price_per_unit=Decimal("25.00"),
                minimum_investment=Decimal("5000.00"),
                type="Education Technology",
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=60),
                status="approved"
            )
            deals.append(deal7)

            deal8 = Deal.objects.create(
                startup=startup,
                name="QuantumCore Series A",
                description="Practical quantum computing solutions",
                content=(
                    "QuantumCore is developing room-temperature quantum computers for commercial applications. Our breakthrough in qubit stability enables practical quantum computing "
                    "solutions for optimization, cryptography, and drug discovery. Unlike traditional quantum systems requiring extreme cooling, QuantumCore's room-temperature design dramatically "
                    "reduces operational complexity and costs, making quantum technology accessible to a wider audience. \n\n"
                    "Our platforms are tailored for industry-specific needs, providing unparalleled computational power for logistics, financial modeling, and material science. "
                    "QuantumCore collaborates with leading research institutions and multinational corporations to co-develop applications that address real-world challenges. "
                    "Additionally, we are investing in developer-friendly tools and training programs to foster an ecosystem of innovation around quantum computing. "
                    "With a robust intellectual property portfolio and a vision for scalable, practical solutions, QuantumCore is poised to redefine industries with quantum advancements."
                ),
                image_background=create_placeholder_file("QuantumCore", "quantumcore_background.png"),
                image_logo=create_placeholder_file("QuantumCore", "quantumcore_logo.png"),
                image_content=create_placeholder_file("QuantumCore", "quantumcore_content.png"),
                dataroom=create_placeholder_file("QuantumCore", "quantumcore_dataroom.pdf"),
                target_amount=Decimal("15000000.00"),
                price_per_unit=Decimal("300.00"),
                minimum_investment=Decimal("30000.00"),
                type="Quantum Computing",
                start_date=timezone.now() - timedelta(days=5),
                end_date=timezone.now() + timedelta(days=85),
                status="approved"
            )
            deals.append(deal8)

            deal9 = Deal.objects.create(
                startup=startup,
                name="AquaTech Ventures Series A",
                description="Revolutionizing water purification technology",
                content=(
                    "AquaTech Ventures is transforming the way we access and utilize clean water with advanced purification and desalination technologies. "
                    "Our proprietary filtration systems use graphene-based membranes that achieve 99.9% impurity removal, ensuring safe drinking water in areas affected by pollution and scarcity. "
                    "Our scalable desalination plants are designed to be energy-efficient, making seawater a viable resource for sustainable communities worldwide. \n\n"
                    "In addition to industrial applications, AquaTech’s smart water management systems employ AI-driven analytics to monitor usage patterns and predict shortages, "
                    "helping municipalities optimize water distribution. We also collaborate with NGOs and governments to implement portable purification units for disaster relief, "
                    "ensuring clean water access during emergencies. As water becomes one of the most critical resources of the 21st century, AquaTech Ventures is dedicated to pioneering "
                    "solutions that secure this vital resource for future generations."
                ),
                image_background=create_placeholder_file("AquaTech", "aquatech_background.jpg"),
                image_logo=create_placeholder_file("AquaTech", "aquatech_logo.png"),
                image_content=create_placeholder_file("AquaTech", "aquatech_content.png"),
                dataroom=create_placeholder_file("AquaTech", "aquatech_dataroom.pdf"),
                target_amount=Decimal("10000000.00"),
                price_per_unit=Decimal("50.00"),
                minimum_investment=Decimal("10000.00"),
                type="Water Technology",
                start_date=timezone.now() - timedelta(days=15),
                end_date=timezone.now() + timedelta(days=60),
            )
            deals.append(deal9)

            deal10 = Deal.objects.create(
                startup=startup,
                name="NeuroNet Seed Round",
                description="AI-powered neuroscience breakthroughs",
                content=(
                    "NeuroNet is leading the charge in neuroscience with AI-powered platforms designed to unlock the mysteries of the human brain. "
                    "Our flagship product, SynapseAI™, provides researchers with tools to simulate neural activity, accelerating discoveries in mental health, neurodegenerative diseases, and cognitive enhancement. "
                    "NeuroNet’s technology has already helped identify biomarkers for conditions like Alzheimer’s and Parkinson’s, enabling earlier and more accurate diagnoses. \n\n"
                    "Our collaborations with leading hospitals and academic institutions allow us to bring cutting-edge research directly to clinical trials, bridging the gap between theory and practice. "
                    "Beyond healthcare, NeuroNet is innovating brain-computer interfaces that empower individuals with physical disabilities, enabling greater autonomy and interaction. "
                    "With a robust commitment to ethical AI, NeuroNet ensures that advancements are implemented responsibly, prioritizing human welfare above all else."
                ),
                image_background=create_placeholder_file("NeuroNet", "neuronet_background.jpg"),
                image_logo=create_placeholder_file("NeuroNet", "neuronet_logo.png"),
                image_content=create_placeholder_file("NeuroNet", "neuronet_content.png"),
                dataroom=create_placeholder_file("NeuroNet", "neuronet_dataroom.pdf"),
                target_amount=Decimal("7000000.00"),
                price_per_unit=Decimal("75.00"),
                minimum_investment=Decimal("15000.00"),
                type="Neuroscience AI",
                start_date=timezone.now() - timedelta(days=20),
                end_date=timezone.now() + timedelta(days=90),
            )
            deals.append(deal10)

            deal11 = Deal.objects.create(
                startup=startup,
                name="AgroFusion Series B",
                description="Innovating sustainable agriculture technology",
                content=(
                    "AgroFusion is a pioneer in sustainable agriculture technology, creating solutions that enhance crop yields while protecting the environment. "
                    "Our precision farming tools leverage satellite imagery and IoT sensors to monitor soil health, optimize irrigation, and reduce pesticide use. "
                    "AgroFusion’s bioengineered seeds are designed to thrive in arid and nutrient-depleted soils, addressing food security challenges worldwide. \n\n"
                    "In addition, our mobile app platform empowers farmers with real-time data on weather patterns, pest risks, and market prices, enabling informed decisions. "
                    "We also focus on regenerative farming practices that restore soil health and sequester carbon, contributing to climate change mitigation. "
                    "With a vision to transform agriculture into a sustainable and profitable industry, AgroFusion is committed to innovation and collaboration at every level of the supply chain."
                ),
                image_background=create_placeholder_file("AgroFusion", "agrofusion_background.jpg"),
                image_logo=create_placeholder_file("AgroFusion", "agrofusion_logo.png"),
                image_content=create_placeholder_file("AgroFusion", "agrofusion_content.jpeg"),
                dataroom=create_placeholder_file("AgroFusion", "agrofusion_dataroom.pdf"),
                target_amount=Decimal("20000000.00"),
                price_per_unit=Decimal("100.00"),
                minimum_investment=Decimal("20000.00"),
                type="Agriculture Technology",
                start_date=timezone.now() - timedelta(days=10),
                end_date=timezone.now() + timedelta(days=75),
            )
            deals.append(deal11)

            deal12 = Deal.objects.create(
                startup=startup,
                name="CleanWave Pre-Series A",
                description="Next-gen ocean cleanup technology",
                content=(
                    "CleanWave is revolutionizing ocean cleanup efforts with autonomous systems designed to remove plastic waste and restore marine ecosystems. "
                    "Our robotic fleets, powered by renewable energy, can operate continuously to collect debris and sort it for recycling. CleanWave’s innovative nanotechnology-based filters "
                    "prevent microplastics from reaching marine food chains, safeguarding aquatic life. \n\n"
                    "In partnership with coastal communities, CleanWave implements waste reduction programs and educates the public on sustainable practices. "
                    "Our advanced data analytics platform tracks pollution hotspots, enabling targeted cleanup efforts and policy recommendations. By addressing both prevention and remediation, "
                    "CleanWave is making significant strides toward a plastic-free ocean and a healthier planet."
                ),
                image_background=create_placeholder_file("CleanWave", "cleanwave_background.jpeg"),
                image_logo=create_placeholder_file("CleanWave", "cleanwave_logo.png"),
                image_content=create_placeholder_file("CleanWave", "cleanwave_content.jpeg"),
                dataroom=create_placeholder_file("CleanWave", "cleanwave_dataroom.pdf"),
                target_amount=Decimal("8000000.00"),
                price_per_unit=Decimal("60.00"),
                minimum_investment=Decimal("12000.00"),
                type="Environmental Technology",
                start_date=timezone.now() - timedelta(days=5),
                end_date=timezone.now() + timedelta(days=85),
            )
            deals.append(deal12)

            return deals

        startup_id = "35cde01a-fd69-442c-904a-bd289595bbdc"
        mock_deals = create_mock_deals(startup_id)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(mock_deals)} mock deals for startup with ID: {startup_id}"
            )
        )
