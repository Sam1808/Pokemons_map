import folium

from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
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
        pokemon_image_url = None #TODO: Just ask me to optimize it!
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
        requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    except Pokemon.MultipleObjectsReturned:
        return HttpResponseNotFound('<h1>Exception.More than one object is found.</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    requested_pokemons_entities = requested_pokemon.pokemon_entities.all()
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

    if requested_pokemon.previous_evolutions:
        previous_evolutions_absolute_url = request.build_absolute_uri(requested_pokemon.previous_evolutions.image.url)
        pokemon["previous_evolution"] = {
                "title_ru": requested_pokemon.previous_evolutions.title,
                "pokemon_id": requested_pokemon.previous_evolutions.id,
                "img_url": previous_evolutions_absolute_url,
            }

    if requested_pokemon.next_evolutions.all():
        next_evolutions = requested_pokemon.next_evolutions.all()[0]
        next_evolutions_absolute_url = request.build_absolute_uri(next_evolutions.image.url)
        pokemon["next_evolution"]={
            "title_ru": next_evolutions.title,
            "pokemon_id": next_evolutions.id,
            "img_url": next_evolutions_absolute_url,
        }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
