

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from app.layers.utilities.translator import fromRequestIntoCard
import requests
from app.models import Favourite

def getAllImages():
    """
    Esta función obtiene todas las imágenes de la API de Rick & Morty y las convierte
    en instancias del modelo Favourite.
    """
    url = 'https://rickandmortyapi.com/api/character/'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json()['results']
        favourites = []
        for result in results:
            favourite = Favourite(
                url=result['image'],
                name=result['name'],
                status=result['status'],
                last_location=result['location']['name'],
                first_seen=result.get('first_episode', 'N/A'),  # Usamos .get() para evitar KeyError
                user=None  # Si se desea asociar a un usuario, hacerlo aquí
            )
            favourites.append(favourite)
        
        return favourites
    else:
        return []  # Si la respuesta de la API no es exitosa, devolver lista vacía

def search_images(query):
    """
    Busca imágenes que coincidan con el término de búsqueda usando la API de Rick & Morty.
    """
    url = f'https://rickandmortyapi.com/api/character/?name={query}'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json()['results']
        favourites = []
        for result in results:
            favourite = Favourite(
                url=result['image'],
                name=result['name'],
                status=result['status'],
                last_location=result['location']['name'],
                first_seen=result.get('first_episode', 'N/A'),  # Usamos .get() para evitar KeyError
                user=None  # Asociar usuario si es necesario
            )
            favourites.append(favourite)
        
        return favourites
    else:
        return []  # Si la respuesta de la API no es exitosa, devolver lista vacía
#Agregamos las funciones para crear la seccion FAVORITOS
def getuserfavourites(user):
    """
    Obtiene los favoritos de un usuario.
    """
    return Favourite.objects.filter(user=user)

def addfavourite(user, image_id): 
    """
    Agrega una imagen a los favoritos del usuario.
    """
    Favourite.objects.create(user=user, id=image_id) #Guarda favorito en la base de datos

def removefavourite(user, image_id):
    """
    Elimina una imagen de los favoritos del usuario.
    """
    Favourite.objects.filter(user=user, id=image_id).delete()

def isfavourite(user, image_id):# Verificamos si una imagen es favorita del usuario
    
    return Favourite.objects.filter(user=user, id=image_id).exists()