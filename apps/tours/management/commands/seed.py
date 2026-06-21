from django.core.management.base import BaseCommand
from apps.tours.models import Tour


class Command(BaseCommand):

    help = "Tạo dữ liệu mẫu"

    def handle(self, *args, **kwargs):

        tours = [

            {
                "name": "Tour Đà Nẵng 3N2Đ",
                "destination": "Đà Nẵng",
                "price": 3500000,
                "duration": 3,
                "slots": 20,
                "description": "Khám phá Bà Nà Hills và biển Mỹ Khê",
                "featured": True
            },

            {
                "name": "Tour Đà Lạt 4N3Đ",
                "destination": "Đà Lạt",
                "price": 4200000,
                "duration": 4,
                "slots": 15,
                "description": "Khám phá thành phố ngàn hoa",
                "featured": True
            },

            {
                "name": "Tour Phú Quốc 3N2Đ",
                "destination": "Phú Quốc",
                "price": 5500000,
                "duration": 3,
                "slots": 18,
                "description": "Khám phá biển đảo Phú Quốc",
                "featured": True
            },

            {
                "name": "Tour Sa Pa 3N2Đ",
                "destination": "Sa Pa",
                "price": 3200000,
                "duration": 3,
                "slots": 25,
                "description": "Khám phá Fansipan",
                "featured": False
            },

            {
                "name": "Tour Nha Trang 3N2Đ",
                "destination": "Nha Trang",
                "price": 4800000,
                "duration": 3,
                "slots": 20,
                "description": "Khám phá VinWonders và biển Nha Trang",
                "featured": True
            },

            {
                "name": "Tour Hà Giang 4N3Đ",
                "destination": "Hà Giang",
                "price": 3900000,
                "duration": 4,
                "slots": 15,
                "description": "Chinh phục đèo Mã Pí Lèng và cao nguyên đá Đồng Văn",
                "featured": True
            },

            {
                "name": "Tour Hạ Long 2N1Đ",
                "destination": "Hạ Long",
                "price": 2800000,
                "duration": 2,
                "slots": 30,
                "description": "Du thuyền khám phá Vịnh Hạ Long",
                "featured": False
            },

            {
                "name": "Tour Huế 3N2Đ",
                "destination": "Huế",
                "price": 3400000,
                "duration": 3,
                "slots": 22,
                "description": "Khám phá Đại Nội và lăng tẩm triều Nguyễn",
                "featured": False
            },

            {
                "name": "Tour Hội An 2N1Đ",
                "destination": "Hội An",
                "price": 2600000,
                "duration": 2,
                "slots": 25,
                "description": "Dạo phố cổ Hội An và thưởng thức ẩm thực địa phương",
                "featured": True
            },

            {
                "name": "Tour Côn Đảo 3N2Đ",
                "destination": "Côn Đảo",
                "price": 6200000,
                "duration": 3,
                "slots": 12,
                "description": "Khám phá biển đảo và di tích lịch sử Côn Đảo",
                "featured": True
            },

            {
                "name": "Tour Mộc Châu 2N1Đ",
                "destination": "Mộc Châu",
                "price": 2400000,
                "duration": 2,
                "slots": 18,
                "description": "Ngắm đồi chè và mùa hoa Mộc Châu",
                "featured": False
            },

            {
                "name": "Tour Cần Thơ 2N1Đ",
                "destination": "Cần Thơ",
                "price": 2200000,
                "duration": 2,
                "slots": 20,
                "description": "Khám phá chợ nổi Cái Răng và miền Tây sông nước",
                "featured": False
            }

        ]

        created = 0

        for t in tours:

            obj, was_created = Tour.objects.get_or_create(
                name=t["name"],
                defaults=t
            )

            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Đã tạo {created} tour mới"
            )
        )
