Парсер, который собирает все объявления с сайта mubawab.ma.

Запуск:
1. Установить требующиеся зависимости: `pip install aiohttp aiohttp-retry lxml pyppeteer tqdm`
2. Запустить `main.py` и дождаться конца выполнения программы.

После выполнения программы в директории `data` появятся два файла: `advs.json` и `new_advs.json`. Оба файла - это список объектов `Advertisement` (`list[Advertisement]`).
1. В `advs.json` содержится список всех объявлений из разделов "For Sale" (https://www.mubawab.ma/en/sc/apartments-for-sale) и "For Rent" (https://www.mubawab.ma/en/sc/apartments-for-rent).
Если объявление было взято из раздела "For Rent", то цена будет записана в поле "for_rent". Иначе оно будет пустым.
2. В `new_advs.json` содержится список всех объявлений из раздела "New Homes" (https://www.mubawab.ma/en/listing-promotion).

Описание всех полей объекта `Advertisement` смотрите в `parser/advertisement.py`

Для выполнения парсинга требуется примерно 20-30 минут в зависимости от мощности железа.