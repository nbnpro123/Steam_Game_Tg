import requests
import time


def get_steam_games_api(region='us', language='english', category='topsellers'):
    """Получение списка игр через Steam API с учетом категории"""
    # API для получения категорий
    api_url = f"https://store.steampowered.com/api/featuredcategories?cc={region}&l={language}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get(api_url, headers=headers)
    games = []

    if response.status_code == 200:
        data = response.json()

        # Выбираем категорию в зависимости от запроса
        category_data = None

        if category == 'topsellers':
            category_data = data.get('topsellers', {}).get('items', [])
        elif category == 'specials':
            category_data = data.get('specials', {}).get('items', [])
        elif category == 'coming_soon':
            category_data = data.get('coming_soon', {}).get('items', [])
        else:
            # По умолчанию берем topsellers
            category_data = data.get('topsellers', {}).get('items', [])

        if category_data:
            print(f"Найдено {len(category_data)} игр в категории {category}")

            for item in category_data[:20]:  # Ограничиваем 20 играми
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
                            is_free = game_info.get('is_free', False)

                            if is_free:
                                price_str = 'Free'
                                discount = 'Free'
                            elif price_info:
                                price = price_info.get('final_formatted', 'N/A')
                                discount_percent = price_info.get('discount_percent', 0)
                                discount = f"-{discount_percent}%"
                                original_price = price_info.get('initial_formatted', price)

                                # Форматируем цену
                                if discount_percent > 0:
                                    price_str = f"{original_price} → {price} ({discount})"
                                else:
                                    price_str = price
                                    discount = '0%'
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

                            # Описание (сокращенное)
                            short_description = game_info.get('short_description', '')
                            if len(short_description) > 150:
                                short_description = short_description[:150] + '...'

                            games.append({
                                'appid': app_id,
                                'title': title,
                                'price': price_str,
                                'discount': discount,
                                'discount_percent': discount_percent if price_info else 0,
                                'is_free': is_free,
                                'release_date': release_date,
                                'genres': ', '.join(genres),
                                'metacritic_score': metacritic,
                                'short_description': short_description,
                                'url': f"https://store.steampowered.com/app/{app_id}"
                            })

                            print(f"✓ {title} - {price_str}")
                        else:
                            print(f"✗ Не удалось получить данные для AppID: {app_id}")
                    else:
                        print(f"✗ Ошибка запроса для AppID: {app_id} - {game_response.status_code}")

                except Exception as e:
                    print(f"✗ Ошибка при обработке AppID: {app_id} - {e}")

                time.sleep(0.5)  # Задержка для избежания блокировки

    return games


def get_top_games():
    """Функция для получения топ-игр"""
    games = get_steam_games_api(region='us', category='specials')
    return format_games_list(games, "🎮 ТОП ИГР ПО ПРОДАЖАМ")


def get_discount_games():
    """Функция для получения игр со скидками"""
    all_games = get_steam_games_api(region='us', category='specials')

    # Фильтруем игры со скидкой более 0%
    discount_games = [game for game in all_games if game.get('discount_percent', 0) > 0]

    # Сортируем по размеру скидки (по убыванию)
    discount_games.sort(key=lambda x: x.get('discount_percent', 0), reverse=True)

    return format_games_list(discount_games[:10], "🔥 ТОП ИГР СО СКИДКАМИ")


def get_free_games():
    """Функция для получения бесплатных игр"""
    all_games = get_steam_games_api(region='us', category='specials')

    # Фильтруем бесплатные игры
    free_games = [game for game in all_games if game.get('is_free', False)]

    # Если в топе мало бесплатных игр, попробуем получить больше из разных категорий
    if len(free_games) < 10:
        specials_games = get_steam_games_api(region='us', category='specials')
        free_games.extend([game for game in specials_games if game.get('is_free', False)])

    # Убираем дубликаты по appid
    seen_ids = set()
    unique_free_games = []
    for game in free_games:
        if game['appid'] not in seen_ids:
            seen_ids.add(game['appid'])
            unique_free_games.append(game)

    return format_games_list(unique_free_games[:20], "🆓 ТОП БЕСПЛАТНЫХ ИГР")


def format_games_list(games, title):
    """Форматирование списка игр для вывода"""
    if not games:
        return f"{title}\n\n😔 Сейчас нет игр в этой категории. Попробуйте позже!"

    game_top = []
    for i, game in enumerate(games[:20], 1):
        # Определяем эмодзи для типа игры
        if game.get('is_free'):
            price_emoji = "🆓"
        elif game.get('discount_percent', 0) > 0:
            price_emoji = "🔥"
        else:
            price_emoji = "💰"

        # Формируем отформатированную строку для каждой игры
        game_info = (
            f"{i}. {price_emoji} *{game['title']}*\n"
            f"   💰 Цена: {game['price']}\n"
        )

        # Добавляем информацию о скидке, если есть
        if game.get('discount_percent', 0) > 0:
            game_info += f"   🏷️ Скидка: {game['discount']}\n"

        game_info += (
            f"   🎭 Жанры: {game.get('genres', 'N/A')}\n"
        )

        # Добавляем рейтинг, если есть
        if game.get('metacritic_score', 'N/A') != 'N/A':
            game_info += f"   ⭐ Рейтинг: {game['metacritic_score']}/100\n"

        # Добавляем краткое описание, если есть
        if game.get('short_description'):
            game_info += f"   📝 {game['short_description']}\n"

        game_info += f"   🔗 [Ссылка на Steam]({game['url']})\n"

        game_top.append(game_info)

    return f"{title}\n\n" + "\n".join(game_top)


if __name__ == "__main__":
    # Тестирование функций
    print("=== Топ игр ===")
    top_games = get_top_games()
    print(top_games[:500])  # Выводим только начало

    print("\n=== Игры со скидками ===")
    discount_games = get_discount_games()
    print(discount_games[:500])

    print("\n=== Бесплатные игры ===")
    free_games = get_free_games()
    print(free_games[:500])
