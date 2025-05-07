import firebase_admin
from firebase_admin import credentials, db
import requests
from bs4 import BeautifulSoup

# Firebase Initialization
cred = credentials.Certificate("firebase-adminsdk-key2.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dbproject-c9527-default-rtdb.firebaseio.com/'
})

# Firebase References
flourandspice_ref = db.reference("flourandspice_recipes")
masala_tv_ref = db.reference("masala_tv_recipes")



def scrape_instructions_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Specific logic for Hum Masala
        method_section = soup.find('div', {'class': 'tab-pane fade show active p-3', 'id': 'english'})
        if method_section:
            ingredients_div = method_section.find('div', {'class': 'ingredients_div'})
            if ingredients_div:
                # Safely find the next sibling after ingredients_div only
                next_sibling = ingredients_div.find_next_sibling()
                while next_sibling and next_sibling.name != 'div':
                    next_sibling = next_sibling.find_next_sibling()

                if next_sibling:
                    instructions = []
                    for tag in next_sibling.find_all('p', recursive=False):
                        # Stop if <p>&nbsp;</p> encountered
                        if tag.get_text(strip=True) in ['\xa0', '']:
                            break
                        instructions.append(tag.get_text(strip=True))
                    return '\n'.join(instructions)

        # Fallback: General-purpose scraping
        possible_containers = soup.find_all(['div', 'section', 'ol', 'ul'],
                                            class_=lambda x: x and 'instruction' in x.lower())
        if not possible_containers:
            possible_containers = soup.find_all(['div', 'section', 'ol', 'ul'],
                                                id=lambda x: x and 'instruction' in x.lower())

        instruction_elements = []
        for container in possible_containers:
            instruction_elements.extend(container.find_all('li'))

        if instruction_elements:
            instructions = [li.get_text(strip=True) for li in instruction_elements]
            return '\n'.join(instructions)

        return "Instructions not found."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
def search_recipes_by_ingredients(ingredients_list):
    ingredients_list = [ingredient.strip().lower() for ingredient in ingredients_list]

    flourandspice_recipes = flourandspice_ref.get() or {}
    masala_tv_recipes = masala_tv_ref.get() or {}
    all_recipes = {**flourandspice_recipes, **masala_tv_recipes}

    exact_match_recipes = []
    partial_match_recipes = []

    for recipe_title, recipe_data in all_recipes.items():
        recipe_ingredients = recipe_data.get("ingredients", "").lower()
        matched_ingredients_count = sum(1 for ingredient in ingredients_list if ingredient in recipe_ingredients)

        url = recipe_data.get("url", "")
        if not url:
            continue

        recipe_info = {
            "title": recipe_title,
            "url": url,
            "ingredients": recipe_data.get("ingredients", "No ingredients"),
        }

        if matched_ingredients_count == len(ingredients_list):
            exact_match_recipes.append(recipe_info)
        elif matched_ingredients_count >= 2:
            recipe_info["matched_count"] = matched_ingredients_count
            partial_match_recipes.append(recipe_info)

    if exact_match_recipes:
        print(f"\nFound {len(exact_match_recipes)} exact matching recipes:\n")
        for i, recipe in enumerate(exact_match_recipes[:5]):
            print(f"{i + 1}. {recipe['title']}")
            print(f"   Ingredients: {recipe['ingredients']}")
            print(f"   URL: {recipe['url']}")
            print("   Instructions (scraped):")
            print(scrape_instructions_from_url(recipe['url']))

            print("\n")
    elif partial_match_recipes:
        partial_match_recipes.sort(key=lambda x: x["matched_count"], reverse=True)
        print(f"\nFound {len(partial_match_recipes)} partial matching recipes:\n")
        for i, recipe in enumerate(partial_match_recipes[:5]):
            print(f"{i + 1}. {recipe['title']}")
            print(f"   Matched Ingredients: {recipe['matched_count']}")
            print(f"   Ingredients: {recipe['ingredients']}")
            print(f"   URL: {recipe['url']}")
            print("   Instructions (scraped):")
            print(scrape_instructions_from_url(recipe['url']))

            print("\n")
    else:
        print("No recipes found that match at least two of the ingredients.")


if __name__ == "__main__":
    user_input = input("Enter ingredients separated by commas: ")
    ingredients_list = [ingredient.strip() for ingredient in user_input.split(",")]
    search_recipes_by_ingredients(ingredients_list)