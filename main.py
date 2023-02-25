import asyncio
from asyncio.coroutines import iscoroutine
import json

from tqdm import tqdm

from parser.browser import create_browser
from parser.advertisement import Advertisement, AdvertisementType
from parser.parser import Parser

URLS = {
    AdvertisementType.APARTMENT: {
        'for_sale': 'https://www.mubawab.ma/en/sc/apartments-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/apartments-for-rent:o:n'
    },
    AdvertisementType.HOUSE: {
        'for_sale': 'https://www.mubawab.ma/en/sc/houses-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/houses-for-rent:o:n',
    },
    AdvertisementType.LUXURY: {
        'for_sale': 'https://www.mubawab.ma/en/sc/villas-and-luxury-homes-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/villas-and-luxury-homes-for-rent:o:n',
    },
    AdvertisementType.RIADS: {
        'for_sale': 'https://www.mubawab.ma/en/sc/riads-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/riads-for-rent:o:n',
    },
    AdvertisementType.COMMERCIAL: {
        'for_sale': 'https://www.mubawab.ma/en/sc/commercial-property-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/commercial-property-for-rent:o:n',
    },
    AdvertisementType.OFFICE_SPACE: {
        'for_sale': 'https://www.mubawab.ma/en/sc/offices-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/cc/rent-all:o:n:sc:office-rent',
    },
    AdvertisementType.LAND: {
        'for_sale': 'https://www.mubawab.ma/en/sc/land-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/land-for-rent:o:n',
    },
    AdvertisementType.FARM: {
        'for_sale': 'https://www.mubawab.ma/en/sc/farms-for-sale:o:n',
        'for_rent': 'https://www.mubawab.ma/en/sc/farms-for-rent:o:n',
    },
}

NEW_HOMES_URLS = {
    AdvertisementType.APARTMENT: 'https://www.mubawab.ma/en/listing-promotion:scat:apartments-for-sale',
    AdvertisementType.COMMERCIAL: 'https://www.mubawab.ma/en/listing-promotion:scat:commercial-property-for-sale',
    AdvertisementType.HOUSE: 'https://www.mubawab.ma/en/listing-promotion:scat:houses-for-sale',
    AdvertisementType.LAND: 'https://www.mubawab.ma/en/listing-promotion:scat:land-for-sale',
    AdvertisementType.LUXURY: 'https://www.mubawab.ma/en/listing-promotion:scat:villas-and-luxury-homes-for-sale',
    AdvertisementType.OFFICE_SPACE: 'https://www.mubawab.ma/en/listing-promotion:scat:offices-for-sale'
}


def write_advs_to_json(advs, filepath):
    advs_json = [a.__dict__ for a in advs]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(advs_json, f, ensure_ascii=False)


async def main():
    max_threads = 60
    browser = await create_browser(max_threads)
    async with Parser(browser) as client:
        semaphore = asyncio.Semaphore(max_threads)
        coros = []
        pbar = tqdm().__enter__()
        # Получаем ссылки на все объявления из разделов "For Rent" и "For Sale" и добавлем
        # в очередь обрбаотку каждой ссылки.
        for property_type, urls in URLS.items():
            for_sale_url = urls['for_sale']
            for_rent_url = urls['for_rent']

            advs = await client.get_all_base_advs(property_type, for_sale_url)
            for adv in advs:
                coros.append(client.parse_adv(adv, semaphore, pbar))

            advs = await client.get_all_base_advs(property_type, for_rent_url)
            for adv in advs:
                coros.append(client.parse_adv(adv, semaphore, pbar, for_rent=True))

        # То же самое, но с разделом "New Homes".
        for property_type, url in NEW_HOMES_URLS.items():
            advs = await client.get_all_base_advs(property_type, url)
            for adv in advs:
                coros.append(client.parse_new_adv(adv, semaphore, pbar))

        coros = coros
        pbar.total = len(coros)
        print('\nПолучаю информацию со всех объявлений сайта...')
        all_advs = await asyncio.wait_for(asyncio.gather(*coros), timeout=None)

        # Отделяем объявления и раздела "New Homes".
        advs = []
        new_advs = []
        for result in all_advs:
            if type(result) is Advertisement:
                adv = result
                if adv.new:
                    new_advs.append(adv)
                else:
                    advs.append(adv)
            # Объявление убрано.
            elif type(result) is str:
                adv_url = result
                for i, adv in reversed(list(enumerate(advs))):
                    if adv.url == adv_url:
                        advs.pop(i)
            elif iscoroutine(result):
                coros.append(result)

        write_advs_to_json(advs, 'data/advs.json')
        write_advs_to_json(new_advs, 'data/new_advs.json')


if __name__ == '__main__':
    asyncio.run(main())
