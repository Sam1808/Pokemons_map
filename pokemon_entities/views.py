import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entities = PokemonEntity.objects.all()
    for pokemon in pokemons_entities:
        pokemon_absolute_url = request.build_absolute_uri(pokemon.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon.lat, pokemon.lon, pokemon.pokemon, pokemon_absolute_url)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_image_url = None #TODO: Optimize it
        if pokemon.image:
            pokemon_image_url = pokemon.image.url

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    try:
        requested_pokemon = Pokemon.objects.filter(id=pokemon_id)[0]
    except IndexError:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    requested_pokemons_entities = PokemonEntity.objects.filter(pokemon = requested_pokemon)
    pokemon_absolute_url = request.build_absolute_uri(requested_pokemon.image.url)


    for pokemon_entity in requested_pokemons_entities:

        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, pokemon_absolute_url)

    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": pokemon_absolute_url,
    }

    if requested_pokemon.previous_evolution:

        previous_evolution_absolute_url = request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
        pokemon["previous_evolution"] = {
                "title_ru": requested_pokemon.previous_evolution.title,
                "pokemon_id": requested_pokemon.previous_evolution.id,
                "img_url": previous_evolution_absolute_url,
            }



    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
