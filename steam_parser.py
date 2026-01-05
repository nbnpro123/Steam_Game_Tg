import requests




url = f"https://store.steampowered.com/appreviews/236390?json=1&language=all&purchase_type=all"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    if 'query_summary' in data:
        review_score = data['query_summary']['review_score']
        print(review_score)

import requests
import time


def get_top_sellers_api(region='us', language='english'):
    """Получение топ-продаж через Steam API с учетом региона"""
    # API для получения топ-продаж
    top_sellers_url = f"https://store.steampowered.com/api/featuredcategories?cc={region}&l={language}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(top_sellers_url, headers=headers)
    top_games = []

    if response.status_code == 200:
        data = response.json()

        # Попробуем разные способы получения списка игр
        top_sellers = None

        # Вариант 1: из раздела topsellers
        if 'topsellers' in data:
            top_sellers = data['topsellers'].get('items', [])
        # Вариант 2: из featured_win
        elif 'featured_win' in data:
            top_sellers = data['featured_win'].get('items', [])
        # Вариант 3: из specials
        elif 'specials' in data:
            top_sellers = data['specials'].get('items', [])

        if top_sellers:
            print(f"Найдено {len(top_sellers)} игр в топ-продажах")

            for item in top_sellers[:10]:  # Для начала возьмем только 10
                app_id = item.get('id')
                if not app_id:
                    continue

                print(f"Получаем информацию для AppID: {app_id}...")

                # Получаем детальную информацию об игре
                game_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc={region}&l={language}"

                try:
                    game_response = requests.get(game_url, headers=headers, timeout=10)

                    if game_response.status_code == 200:
                        game_data = game_response.json()

                        if str(app_id) in game_data and game_data[str(app_id)].get('success'):
                            game_info = game_data[str(app_id)].get('data', {})

                            title = game_info.get('name', 'Unknown')

                            # Получаем цену
                            price_info = game_info.get('price_overview', {})
                            if price_info:
                                price = price_info.get('final_formatted', 'N/A')
                                discount = f"-{price_info.get('discount_percent', 0)}%"
                                original_price = price_info.get('initial_formatted', price)

                                # Форматируем цену
                                if discount != '-0%':
                                    price_str = f"{original_price} → {price} ({discount})"
                                else:
                                    price_str = price
                            else:
                                # Проверяем, бесплатная ли игра
                                if game_info.get('is_free', False):
                                    price_str = 'Free'
                                else:
                                    price_str = 'N/A'
                                discount = '0%'

                            # Дата выхода
                            release_info = game_info.get('release_date', {})
                            if isinstance(release_info, dict):
                                release_date = release_info.get('date', 'Unknown')
                            else:
                                release_date = 'Unknown'

                            # Жанры
                            genres = []
                            if 'genres' in game_info:
                                genres = [genre['description'] for genre in game_info['genres'][:3]]

                            # Рейтинг
                            metacritic = game_info.get('metacritic', {}).get('score', 'N/A')

                            top_games.append({
                                'appid': app_id,
                                'title': title,
                                'price': price_str,
                                'discount': discount,
                                'release_date': release_date,
                                'genres': ', '.join(genres),
                                'metacritic_score': metacritic,
                                'url': f"https://store.steampowered.com/app/{app_id}"
                            })

                            print(f"✓ {title} - {price_str}")
                        else:
                            print(f"✗ Не удалось получить данные для AppID: {app_id}")
                    else:
                        print(f"✗ Ошибка запроса для AppID: {app_id} - {game_response.status_code}")

                except Exception as e:
                    print(f"✗ Ошибка при обработке AppID: {app_id} - {e}")

                time.sleep(0.5)  # Увеличиваем задержку

    return top_games




# Тестируем оба метода
if __name__ == "__main__":
    print("=== Метод 1: API featured categories ===")
    top_games1 = get_top_sellers_api(region='us')

    print(f"\nНайдено {len(top_games1)} игр через API")
    for i, game in enumerate(top_games1[:20], 1):
        print(f"{i}. {game['title']}")
        print(f"   Цена: {game['price']}")
        print(f"   Жанры: {game.get('genres', 'N/A')}")
        print(f"   Metacritic: {game.get('metacritic_score', 'N/A')}")
        print()






