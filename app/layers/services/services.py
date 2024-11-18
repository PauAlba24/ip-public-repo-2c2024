# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests

def getAllImages(input=None):

    
    url= 'https://rickandmortyapi.com/api/character/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
      
     # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = response.json().get('results',[])
    images = []
    for character in json_collection:
        images.append({
            'name': character.get('name'),
            'status': character.get('status'),
            'url': character.get('image'),
            'last_location': character.get('location', {}).get('name'),
            'first_seen': character.get('episode', [])[0]  # Primer episodio
        })

    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
