# capa de vista/presentación
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# Función que maneja la página principal con imágenes y favoritos del usuario
def home(request):
    # Obtener las imágenes desde la API
    images = services.getAllImages()  # Llama a la función de servicios para obtener imágenes

       
    if request.user.is_authenticated: #Buscamos en service la funcion get user favourites
        favourites = services.getuserfavourites(request.user)
    else:
        favourites = []
#Preparamos el diccionario con las imagenes y los favoritos 
    context = { 
        'images': images,
        'favourites': favourites,
    }
    
    return render(request, 'home.html', context)

# Función que maneja la búsqueda de imágenes
def search(request):
    search_msg = request.POST.get('query', '').strip()

    # Si el texto ingresado no está vacío
    if search_msg != '':
        # Llamar a la función que obtiene las imágenes que coinciden con la búsqueda
        images = services.search_images(search_msg)
        
        # Verificar si el usuario está autenticado para obtener sus favoritos
        if request.user.is_authenticated:
            favourites = services.getuserfavourites(request.user)  # Obtiene favoritos del usuario
        else:
            favourites = []  # Lista vacía si no está autenticado

        # Pasar las imágenes y los favoritos al template `home.html`
        context = {
            'images': images,
            'favourites': favourites,
            'search_msg': search_msg  # Puedes pasar el término de búsqueda para mostrarlo
        }
        return render(request, 'home.html', context)
    else:
        return redirect('home')  # Redirigir a la página de inicio si el campo está vacío

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request): #Completamos la funcion que ya venia
    # Obtener los favoritos del usuario
    favourite_list = services.getuserfavourites(request.user)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == "POST":
        image_id = request.POST.get('image_id')
        services.addfavourite(request.user, image_id)
        return redirect('home')  # Redirige a la página principal o donde convenga

@login_required
def deleteFavourite(request):
    if request.method == "POST":
        image_id = request.POST.get('image_id')
        # Lógica para eliminar el favorito
        services.removefavourite(request.user, image_id)
        return redirect('home')

@login_required
def exit(request):
    logout(request)  # Desconectar al usuario
    return redirect('index')  # Redirigir a la página principal