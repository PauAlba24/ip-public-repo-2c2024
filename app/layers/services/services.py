from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
from app.models import Favourite


def getAllImages(input=None):
    # obtenemos los datos de la API
    json_collection = transport.getAllImages(input) 

    # Lista para almacenar las imágenes convertidas
    images = []
    index = 0

    # Usamos while en vez de for para recorrer los datos
    while index < len(json_collection):  
        images.append(translator.fromRequestIntoCard(json_collection[index]))  # Convertimos cada objeto a una Card
        index += 1
    
    return images
def addfavourite(user, image_id):
    # Obtener la imagen usando el ID
    images = getAllImages(image_id)
    if not images:
        print(f"No se encontró la imagen con id: {image_id}")
        return None

    image = images[0]  # Seleccionamos la primera imagen de la lista

    # Verificamos si el favorito ya existe
    existing_favourite = Favourite.objects.filter(
        user=user,
        url=image.url,
        name=image.name,
        status=image.status,
        last_location=image.last_location,
        first_seen=image.first_seen
    ).first()

    if existing_favourite:
        print("Este favorito ya existe")
        return existing_favourite  # Si ya existe, no lo creamos de nuevo

    # Crear el nuevo favorito si no existe
    favourite = Favourite.objects.create(
        user=user,
        url=image.url,
        name=image.name,
        status=image.status,
        last_location=image.last_location,
        first_seen=image.first_seen
    )
    return favourite
def saveFavourite(request):
     # Transformamos un request del template en una Card.
    fav = translator.fromTemplateIntoCard(request)  
    fav.user = get_user(request)  # Asignamos el usuario correspondiente.
    
    # Guardamos el favorito en la base de datos
    return repositories.saveFavourite(fav)
def getuserfavourites(user):  # Cambié de 'request' a 'user'
    if not user.is_authenticated:  # Verificamos si el usuario está autenticado
        return []
    
    # Obtenemos los favoritos del usuario desde el repositorio
    favourite_list = repositories.getAllFavourites(user)  
    mapped_favourites = []

    # Usamos while en vez de for para recorrer los favoritos
    index = 0
    while index < len(favourite_list):  
        card = translator.fromRepositoryIntoCard(favourite_list[index])  # Convertimos cada favorito en una Card
        mapped_favourites.append(card)
        index += 1

    return mapped_favourites

def deleteFavourite(user, fav_id):
    # Verificamos que el favorito exista
    favourite = Favourite.objects.filter(id=fav_id, user=user).first()  # Filtramos por 'id' y 'user'
    
    if favourite:
        favourite.delete()  # Eliminamos el favorito
        return True  # Indicamos que se eliminó correctamente
    return False  # Si no se encuentra el favorito, no hacemos nada