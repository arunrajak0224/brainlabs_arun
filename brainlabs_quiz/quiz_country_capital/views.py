from django.shortcuts import render
import requests
import random

# Fetch country-capital data from API
def fetch_country_capital():
    api_url = "https://countriesnow.space/api/v0.1/countries/capital"
    response = requests.get(api_url)
    data = response.json()
    country_data = data.get("data", [])
    return {country["name"]: country["capital"] for country in country_data}

# Initialize global variables
country_capital_map = fetch_country_capital()
current_country = random.choice(list(country_capital_map.keys()))
current_correct_capital = country_capital_map[current_country]
result = None

# Main view function
def quiz(request):
    global current_country, current_correct_capital, result
    
    if request.method == "POST":
        guessed_capital = request.POST.get("capital", "").strip()
        correct_capital_normalized = current_correct_capital.strip().lower()
        if guessed_capital.lower() == correct_capital_normalized:
            result = "Correct!"
        else:
            result = f"Incorrect! The capital of {current_country} is {current_correct_capital}."
    
    # Pick a new random country and its corresponding capital for the next question
    current_country = random.choice(list(country_capital_map.keys()))
    current_correct_capital = country_capital_map[current_country]

    return render(request, "quiz/quiz.html", {"country": current_country, "result": result})
