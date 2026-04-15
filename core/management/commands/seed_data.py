from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    AcceptedDonation,
    ChurchHistory,
    ChurchInfo,
    CoreValue,
    HeroSlide,
    SocialLink,
    WeeklyService,
)
from events.models import Event


class Command(BaseCommand):
    help = "Seed initial church content"

    def handle(self, *args, **options):
        info, _ = ChurchInfo.objects.get_or_create(
            name="Immanuel Gospel Ministries",
            defaults={
                "tagline": "Empowering lives through the Word and prayer",
                "description": "Welcome to Immanuel Gospel Ministries, a vibrant Christ-centered family.",
                "location": "Megga, Nderi, Sigona Ward (Sauri)",
                "mission": "To preach the Gospel of Jesus Christ, nurture believers in faith, and empower individuals to live transformed, Christ-centered lives through the Word of God, prayer, and the power of the Holy Spirit.",
                "vision": "To raise a generation of spiritually grounded, empowered believers who impact their communities and the world with the love, truth, and power of Jesus Christ.",
                "reverend_name": "Rev. Samuel Muhindi Mwaura",
                "reverend_bio": "A passionate servant of God dedicated to biblical teaching, prayer, and outreach.",
                "whatsapp_phone": "254700000000",
                "mpesa_paybill": "123456",
                "mpesa_paybill_account": "OFFERING",
                "mpesa_till": "654321",
            },
        )
        if not info.whatsapp_phone:
            ChurchInfo.objects.filter(pk=info.pk).update(whatsapp_phone="254700000000")
        if not info.mpesa_paybill:
            ChurchInfo.objects.filter(pk=info.pk).update(mpesa_paybill="123456")
        if not info.mpesa_paybill_account:
            ChurchInfo.objects.filter(pk=info.pk).update(mpesa_paybill_account="OFFERING")
        if not info.mpesa_till:
            ChurchInfo.objects.filter(pk=info.pk).update(mpesa_till="654321")

        ChurchHistory.objects.get_or_create(
            id=1,
            defaults={
                "content": "Immanuel Gospel Ministries was founded with a passion to spread the Gospel of Jesus Christ and transform lives through the power of God’s Word. Located in Megga, Nderi, Sigona Ward (Sauri), the church began as a small fellowship of believers committed to prayer, biblical teaching, and community outreach. Under the leadership of Rev. Samuel Muhindi Mwaura, the ministry has grown into a vibrant place of worship impacting lives through teaching, worship, deliverance, and outreach programs.",
                "is_published": True,
            },
        )

        values = [
            ("Faith", "Trusting God in all things"),
            ("Holiness", "Living a life that honors God"),
            ("Love", "Serving others with compassion"),
            ("Integrity", "Walking in truth and honesty"),
            ("Prayer", "Dependence on God for everything"),
        ]
        for i, (title, description) in enumerate(values):
            CoreValue.objects.update_or_create(
                title=title,
                defaults={"description": description, "sort_order": i, "is_published": True},
            )

        if not HeroSlide.objects.exists():
            slides = [
                (
                    "Welcome to Immanuel Gospel Ministries",
                    "Growing in faith, prayer, and God's Word together.",
                    "https://images.unsplash.com/photo-1438232992991-995b7058bbb3?auto=format&fit=crop&w=1600&q=80",
                    0,
                ),
                (
                    "Join Us Every Sunday",
                    "Bible study, praise and worship, main service, and deliverance prayers.",
                    "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1600&q=80",
                    1,
                ),
                (
                    "Midweek Biblical Studies",
                    "Wednesday fellowship dedicated to prayer and scripture.",
                    "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1600&q=80",
                    2,
                ),
            ]
            for title, subtitle, url, order in slides:
                HeroSlide.objects.create(
                    title=title,
                    subtitle=subtitle,
                    image_url=url,
                    sort_order=order,
                    is_published=True,
                )

        if not WeeklyService.objects.exists():
            rows = [
                ("Wednesday", "Biblical Studies and Prayers", "3:00 PM - 6:00 PM", 0),
                ("Sunday", "Bible Study", "10:00 AM - 11:00 AM", 1),
                ("Sunday", "Praise and Worship", "11:00 AM - 12:00 PM", 2),
                ("Sunday", "Main Service and Deliverance Prayers", "12:00 PM - 1:30 PM", 3),
            ]
            for day, name, time, order in rows:
                WeeklyService.objects.create(
                    day_label=day,
                    name=name,
                    time_label=time,
                    sort_order=order,
                    is_published=True,
                )

        if not SocialLink.objects.exists():
            SocialLink.objects.create(label="Facebook", url="https://facebook.com/", sort_order=0, is_published=True)
            SocialLink.objects.create(label="YouTube", url="https://youtube.com/", sort_order=1, is_published=True)
            SocialLink.objects.create(label="Instagram", url="https://instagram.com/", sort_order=2, is_published=True)

        donations = [
            (
                AcceptedDonation.Category.CLOTHING,
                "Clothing (all ages)",
                "Clean, gently used shirts, trousers, dresses, and jackets. Seasonal wear welcome.",
                1,
            ),
            (
                AcceptedDonation.Category.FOOTWEAR,
                "Shoes & footwear",
                "Sturdy shoes and sandals in good condition for children and adults.",
                2,
            ),
            (
                AcceptedDonation.Category.TOYS_CHILDREN,
                "Toys for children",
                "Age-appropriate toys, books, and games; no broken or recalled items.",
                3,
            ),
            (
                AcceptedDonation.Category.ADULTS,
                "Toys & gifts for adults",
                "Puzzles, hobby items, and small gifts suitable for adult recipients where appropriate.",
                4,
            ),
            (
                AcceptedDonation.Category.OTHER,
                "Other useful items",
                "School supplies, blankets, and household basics when space allows. Call ahead for large donations.",
                5,
            ),
        ]
        for category, headline, details, sort_order in donations:
            AcceptedDonation.objects.get_or_create(
                headline=headline,
                defaults={
                    "category": category,
                    "details": details,
                    "sort_order": sort_order,
                    "is_published": True,
                },
            )

        Event.objects.get_or_create(
            title="Entrepreneurship & small business seminar",
            defaults={
                "description": "Practical training on starting and growing a small business, budgeting, and integrity in the marketplace — grounded in biblical wisdom.",
                "date": timezone.now() + timezone.timedelta(days=21),
                "location": info.location,
                "kind": Event.Kind.SEMINAR_TRAINING,
                "training_focus": "Entrepreneurship",
                "is_published": True,
            },
        )
        Event.objects.get_or_create(
            title="Youth empowerment workshop",
            defaults={
                "description": "Building confidence, purpose, and godly character for young people through teaching, discussion, and mentorship.",
                "date": timezone.now() + timezone.timedelta(days=35),
                "location": info.location,
                "kind": Event.Kind.SEMINAR_TRAINING,
                "training_focus": "Empowerment",
                "is_published": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))
