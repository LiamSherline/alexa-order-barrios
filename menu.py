"""Menu data for Barrios Mexican Cantina, Oak Ridge TN.

Source of truth: the printed house menu and https://barriosoakridge.com
(scraped 2026-10-02). Prices are stored in integer cents to avoid
float rounding in order totals.

DO NOT invent items or prices here. If the website menu changes, update
this file from the site, not from memory.
"""

from __future__ import annotations

# Locked pricing facts (also asserted in tests):
#   queso 4oz $3.50 / 8oz $7.00 / 16oz $13.00
#   guac  4oz $4.00 / 8oz $8.00 / 16oz $15.00

MENU = {
    "restaurant": "Barrios Mexican Cantina",
    "address": "154 Talmeda Road, Oak Ridge, TN 37830",
    "phone": "(865) 272-5171",
    "categories": [
        {
            "id": "calle_tacos",
            "name": "Calle Tacos",
            "items": [
                {"id": "taco-barbacoa", "name": "Taco Barbacoa", "price_cents": 425},
                {"id": "taco-birria", "name": "Taco Birria", "price_cents": 475},
                {"id": "taco-cachete", "name": "Taco Cachete", "price_cents": 400},
                {"id": "taco-cauliflower", "name": "Taco Cauliflower", "price_cents": 400},
                {"id": "taco-carne-asada", "name": "Taco Carne Asada", "price_cents": 425},
                {"id": "taco-carnitas", "name": "Taco Carnitas", "price_cents": 400},
                {"id": "taco-chorizo", "name": "Taco Chorizo", "price_cents": 400},
                {"id": "taco-hot-chicken", "name": "Taco Hot Chicken", "price_cents": 450},
                {"id": "taco-pickled-hot-chicken", "name": "Taco Pickled Hot Chicken", "price_cents": 450},
                {"id": "taco-lengua", "name": "Taco Lengua", "price_cents": 450},
                {"id": "taco-molida", "name": "Taco Molida", "price_cents": 400},
                {"id": "taco-pollo-asada", "name": "Taco Pollo Asada", "price_cents": 400},
                {"id": "taco-al-pastor", "name": "Al Pastor", "price_cents": 400},
                {"id": "taco-baja-shrimp", "name": "Baja Shrimp", "price_cents": 450},
                {"id": "taco-baja-mahi", "name": "Baja Mahi", "price_cents": 600},
                {"id": "taco-surf-turf", "name": "Surf and Turf", "price_cents": 500},
                {"id": "taco-choripollo", "name": "Choripollo", "price_cents": 425},
                {"id": "taco-campechano", "name": "Campechano", "price_cents": 425},
                {"id": "taco-fajita-chicken", "name": "Fajita Chicken", "price_cents": 425},
                {"id": "taco-fajita-steak", "name": "Fajita Steak", "price_cents": 450},
                {"id": "taco-fajita-shrimp", "name": "Fajita Shrimp", "price_cents": 450},
                {"id": "taco-tripa", "name": "Tripa", "price_cents": 400},
                {"id": "taco-tinga", "name": "Tinga", "price_cents": 400},
            ],
        },
        {
            "id": "plates",
            "name": "Plates",
            "items": [
                {"id": "loaded-burrito", "name": "Loaded Burrito", "price_cents": 1500},
                {"id": "enchiladas-dinner", "name": "Enchiladas Dinner", "price_cents": 1500},
                {"id": "enchiladas-supremas", "name": "Enchiladas Supremas", "price_cents": 1500},
                {"id": "fajita-burrito-dinner", "name": "Fajita Burrito Dinner", "price_cents": 1600},
                {"id": "cheese-steak-burrito", "name": "Cheese Steak Burrito", "price_cents": 1700},
                {"id": "arroz-loco", "name": "Arroz Loco", "price_cents": 1500},
                {"id": "pozole", "name": "Pozole", "price_cents": 1399},
                {"id": "seafood-chimichanga", "name": "Seafood Chimichanga", "price_cents": 1800},
                {"id": "chile-relleno", "name": "Chile Relleno", "price_cents": 1500},
                {"id": "mixto-burrito", "name": "Mixto Burrito", "price_cents": 1700},
                {"id": "california-burrito", "name": "California Burrito", "price_cents": 1300},
                {"id": "surf-turf-cali-burrito", "name": "Surf & Turf Cali Burrito", "price_cents": 1400},
                {"id": "spinach-burrito", "name": "Spinach Burrito", "price_cents": 1400},
                {"id": "veggie-loaded-burrito", "name": "Veggie Loaded Burrito", "price_cents": 1500},
                {"id": "burrito-bowl", "name": "Burrito Bowl", "price_cents": 1500},
                {"id": "birria-tacos-3", "name": "Birria Tacos (3)", "price_cents": 1600},
                {"id": "soggy-tacos-2", "name": "Soggy Tacos (2)", "price_cents": 1600},
                {"id": "mix-and-match-3", "name": "Mix and Match (3)", "price_cents": 1300},
                {"id": "birria-queso-dip", "name": "Birria Queso Dip", "price_cents": 1300},
                {"id": "street-corn-plate", "name": "Street Corn", "price_cents": 500},
            ],
        },
        {
            "id": "sides",
            "name": "Sides",
            "items": [
                {"id": "rice-and-beans", "name": "Rice and Beans", "price_cents": 500},
                {"id": "queso-4oz", "name": "Queso, 4 oz", "price_cents": 350},
                {"id": "queso-8oz", "name": "Queso, 8 oz", "price_cents": 700},
                {"id": "queso-16oz", "name": "Queso, 16 oz", "price_cents": 1300},
                {"id": "guac-4oz", "name": "Guacamole, 4 oz", "price_cents": 400},
                {"id": "guac-8oz", "name": "Guacamole, 8 oz", "price_cents": 800},
                {"id": "guac-16oz", "name": "Guacamole, 16 oz", "price_cents": 1500},
                {"id": "salsa-8oz", "name": "Salsa, 8 oz", "price_cents": 325},
                {"id": "pico-de-gallo", "name": "Pico de Gallo", "price_cents": 75},
                {"id": "street-corn-side", "name": "Street Corn", "price_cents": 500},
            ],
        },
        {
            "id": "lunch",
            "name": "Lunch",
            "items": [
                {"id": "lunch-burrito", "name": "Lunch Burrito", "price_cents": 1000},
                {"id": "speedy-gonzales", "name": "Speedy Gonzales", "price_cents": 1100},
                {"id": "taco-combo-2", "name": "Taco Combo (2)", "price_cents": 1200},
                {"id": "lunch-enchiladas-2", "name": "Lunch Enchiladas (2)", "price_cents": 1100},
                {"id": "lunch-chile-relleno", "name": "Lunch Chile Relleno", "price_cents": 1100},
                {"id": "lunch-fajitas", "name": "Lunch Fajitas", "price_cents": 1200},
            ],
        },
        {
            "id": "kids",
            "name": "Kids",
            "items": [
                {"id": "nino-taco", "name": "Nino Taco", "price_cents": 750},
                {"id": "nino-quesadilla", "name": "Nino Quesadilla", "price_cents": 799},
                {"id": "nino-burrito", "name": "Nino Burrito", "price_cents": 799},
                {"id": "nino-enchilada", "name": "Nino Enchilada", "price_cents": 799},
            ],
        },
        {
            "id": "drinks",
            "name": "Drinks",
            "items": [
                {"id": "casa-margarita", "name": "Casa Margarita", "price_cents": 800},
                {"id": "skinny-margarita", "name": "Skinny Margarita", "price_cents": 800},
                {"id": "spicy-margarita", "name": "Spicy Margarita", "price_cents": 800},
                {"id": "blackberry-margarita", "name": "Blackberry Margarita", "price_cents": 1100},
                {"id": "coconut-lime-margarita", "name": "Coconut Lime Margarita", "price_cents": 1100},
                {"id": "diablo-margarita", "name": "Diablo Margarita", "price_cents": 1000},
                {"id": "top-shelf-margarita", "name": "Top Shelf Margarita", "price_cents": 1200},
                {"id": "smokey-margarita", "name": "Smokey Margarita", "price_cents": 1200},
                {"id": "don-julio-margarita", "name": "Don Julio Margarita", "price_cents": 1600},
                {"id": "lalo", "name": "Lalo", "price_cents": 1600},
                {"id": "purple-haze", "name": "Purple Haze", "price_cents": 1600},
                {"id": "ocho-royal", "name": "Ocho Royal", "price_cents": 1800},
                {"id": "house-margarita-32oz", "name": "House Margarita 32oz", "price_cents": 1500},
                {"id": "spicy-margarita-32oz", "name": "Spicy Margarita 32oz", "price_cents": 1500},
                {"id": "skinny-margarita-32oz", "name": "Skinny Margarita 32oz", "price_cents": 1500},
                {"id": "top-shelf-margarita-32oz", "name": "Top Shelf Margarita 32oz", "price_cents": 2000},
                {"id": "oaxacan", "name": "Oaxacan", "price_cents": 1200},
                {"id": "paloma", "name": "Paloma", "price_cents": 900},
                {"id": "pineapple-paloma", "name": "Pineapple Paloma", "price_cents": 1000},
                {"id": "jungle-bird", "name": "Jungle Bird", "price_cents": 1300},
                {"id": "batanga", "name": "Batanga", "price_cents": 1000},
                {"id": "cazuela", "name": "Cazuela", "price_cents": 1300},
                {"id": "extra-anejo-old-fashioned", "name": "Extra Anejo Old Fashioned", "price_cents": 1300},
                {"id": "azteca-negroni", "name": "Azteca Negroni", "price_cents": 1400},
                {"id": "strawberry-daiquiri", "name": "Strawberry Daiquiri", "price_cents": 1000},
                {"id": "horchata-rum-punch", "name": "Horchata Rum Punch", "price_cents": 1000},
                {"id": "pina-colada", "name": "Pina Colada", "price_cents": 1000},
                {"id": "barrios-mojito", "name": "Barrios Mojito", "price_cents": 1000},
                {"id": "spicy-pina-mule", "name": "Spicy Pina Mule", "price_cents": 1200},
                {"id": "agua-fresca-vodka-cooler", "name": "Agua Fresca Vodka Cooler", "price_cents": 1000},
                {"id": "vanessa-mule", "name": "Vanessa Mule", "price_cents": 1000},
                {"id": "smokey-sunset", "name": "Smokey Sunset", "price_cents": 1200},
                {"id": "whiskey-smash", "name": "Whiskey Smash", "price_cents": 1200},
                {"id": "old-fashioned", "name": "Old Fashioned", "price_cents": 1200},
                {"id": "condesa-gimlet", "name": "Condesa Gimlet", "price_cents": 1400},
                {"id": "gin-con-jamaica", "name": "Gin con Jamaica", "price_cents": 1300},
                {"id": "carajillo", "name": "Carajillo", "price_cents": 1100},
                {"id": "espresso-martini", "name": "Espresso Martini", "price_cents": 1100},
                {"id": "aperol-spritz", "name": "Aperol Spritz", "price_cents": 1000},
                {"id": "tanqueray", "name": "Tanqueray", "price_cents": 700},
                {"id": "condesa", "name": "Condesa", "price_cents": 900},
                {"id": "blantons", "name": "Blantons", "price_cents": 1800},
                {"id": "buffalo-trace", "name": "Buffalo Trace", "price_cents": 800},
                {"id": "bulleit", "name": "Bulleit", "price_cents": 800},
                {"id": "eh-taylor", "name": "EH Taylor", "price_cents": 1300},
                {"id": "elijah-craig", "name": "Elijah Craig", "price_cents": 700},
                {"id": "makers-mark", "name": "Makers Mark", "price_cents": 700},
                {"id": "weller-special-reserve", "name": "Weller Special Reserve", "price_cents": 1200},
                {"id": "weller-12", "name": "Weller 12", "price_cents": 2200},
                {"id": "crown-royal", "name": "Crown Royal", "price_cents": 700},
                {"id": "jack-daniels", "name": "Jack Daniels", "price_cents": 600},
                {"id": "jameson", "name": "Jameson", "price_cents": 700},
                {"id": "cabernet", "name": "Cabernet", "price_cents": 600},
                {"id": "chardonnay", "name": "Chardonnay", "price_cents": 600},
                {"id": "pinot-grigio", "name": "Pinot Grigio", "price_cents": 600},
                {"id": "rose", "name": "Rose", "price_cents": 600},
                {"id": "sauvignon-blanc", "name": "Sauvignon Blanc", "price_cents": 600},
                {"id": "bottled-water", "name": "Bottled Water", "price_cents": 300},
                {"id": "rusa", "name": "Rusa", "price_cents": 600},
                {"id": "horchata", "name": "Horchata", "price_cents": 375},
                {"id": "mexican-coke", "name": "Mexican Coke", "price_cents": 450},
                {"id": "diet-coke", "name": "Diet Coke", "price_cents": 325},
                {"id": "agua-fresca-grande", "name": "Agua Fresca Grande", "price_cents": 575},
            ],
        },
    ],
}

# Flat lookup: item_id -> item dict (with category attached).
ITEMS: dict[str, dict] = {}
for _cat in MENU["categories"]:
    for _item in _cat["items"]:
        ITEMS[_item["id"]] = {**_item, "category": _cat["id"]}


def get_item(item_id: str) -> dict | None:
    """Return the menu item for item_id, or None if it does not exist."""
    return ITEMS.get(item_id)


def format_price(price_cents: int) -> str:
    """Format integer cents as $d.cc for display."""
    return f"${price_cents / 100:.2f}"
