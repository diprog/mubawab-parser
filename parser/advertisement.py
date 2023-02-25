from enum import IntEnum, auto


class AdvertisementType(IntEnum):
    APARTMENT = auto()
    HOUSE = auto()
    LUXURY = auto()
    RIADS = auto()
    COMMERCIAL = auto()
    OFFICE_SPACE = auto()
    LAND = auto()
    FARM = auto()
    NEW = auto()


class Advertisement:
    def __init__(self, property_type: AdvertisementType, **kwargs):
        # Тип недвижимости.
        self.property_type = property_type
        # Объявление из раздела новостроек.
        self.new = kwargs.get('new', False)
        # Ссылка на объявление.
        self.url = kwargs.get('url')
        # Заголовок объявления.
        self.title: str = kwargs.get('title')
        # Описание объявления.
        self.description: str = kwargs.get('description')
        # Общая площадь.
        self.area: int = kwargs.get('area')
        # Этаж.
        self.floor: int = kwargs.get('floor')
        # Количество комнат.
        self.rooms_number: int = kwargs.get('rooms_number')
        # Цена.
        self.price: float = kwargs.get('price')
        self.price_per_day: float = kwargs.get('price_per_day')  # В некоторыъ объявлениях указана только аренда за день.
        self.from_price: float = kwargs.get('from_price')  # В некоторыъ объявлениях указана стартовая цена (начиная от).
        self.rent_price: float = kwargs.get('rent_price')  # Цена аренды, если объявление из раздела "For Rent".
        self.request_price: bool = kwargs.get('request_bool', False)  # Если в объявлении указано "Price on Request"
        # Валюта.
        self.currency: str = kwargs.get('currency')
        # Район.
        self.district: str = kwargs.get('district')
        # Город.
        self.region: str = kwargs.get('region')
        # Как давно было опубликовано.
        # Точно можно узнать только до 6 месяцев. Всё, что больше,
        # будет отображаться в виде "Published more than 6 months ago".
        self.publish_date: str = kwargs.get('publish_date')
        # Номера телефонов, по которым можно связаться.
        self.phone_numbers: list[str] = kwargs.get('phone_numbers')
        # Теги. Пример: ['2600 m²', '1 Piece', '3 Rooms', '1 Bathroom', 'Due for reform']
        self.tags: list[str] = kwargs.get('tags', [])
        # Преимущества. Скриншот: https://ctrl.vi/i/6SkooV3Qb
        self.ad_features: list[str] = kwargs.get('ad_features', [])
        # Наличие пассажирского лифта. Берется из ad_features
        self.elevator: bool | None = kwargs.get('elevator')
        # Координаты территории.
        self.location: list[float, float] = kwargs.get('location')
        # Ссылки на фото.
        self.photos_urls: list[str] = kwargs.get('photos_urls', [])
        # Возраст постройки.
        self.age: int = kwargs.get('age')
