# capa de vista/presentación
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services.services import addfavourite
from app.layers.services.services import deleteFavourite as service_deleteFavourite



def index_page(request):
    return render(request, 'index.html')

# Función que maneja la página principal con imágenes y favoritos del usuario
def home(request):
    # Obtener las imágenes desde la API
    images = services.getAllImages()  # Llama a la función para obtener todas las imágenes

    favourites = services.getuserfavourites(request.user) if request.user.is_authenticated else []
#Preparamos el contexto para la plantilla con las imagenes y los favoritos 
    context = { 
        'images': images,
        'favourites': favourites,
    }
    
    return render(request, 'home.html', context)

# Función que maneja la búsqueda de imágenes
def search(request):
    search_msg = request.POST.get('query', '')

    # Si el texto ingresado no está vacío trae las imágenes y favoritos que estan en services.py,
    # para despues renderizar el template
    if search_msg != '':
        # Llamar a la función que obtiene las imágenes que coinciden con la búsqueda
        images = services.search_images(search_msg)
        
        # Verificar si el usuario está autenticado para obtener sus favoritos
        favourites = services.getuserfavourites(request)
        # Preparar el contexto para pasar a la plantilla
        context = {
            'images': images,
            'favourites': favourites,  
            'search_msg': search_msg  # Mostrar el término de búsqueda al usuario
        }
        return render(request, 'home.html', context)
    
    else:
        # Redirigir a la página de inicio si el campo de búsqueda está vacío
        return redirect('home')

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
        
        # Verificar que el 'image_id' sea válido
        if image_id:
            favourite = services.addfavourite(request.user, image_id)
            if favourite:
                return redirect('home')  # Redirigir a la página de inicio
            else:
                # Puedes agregar un mensaje de error si no se pudo agregar el favorito
                print("Error: El favorito no se agregó correctamente.")
        
    return redirect('home')  # Si no es un POST, redirigimos a la página de inicio

@login_required
def deleteFavourite(request):
    if request.method == "POST":
        image_id = request.POST.get('image_id')  # Asegúrate de que 'image_id' esté bien definido en el formulario
        services.deleteFavourite(request.user, image_id)  # Llama correctamente al servicio
        return redirect('favoritos')  # Redirige a la página de favoritos después de eliminar
@login_required
def exit(request):
    logout(request)  # Desconectar al usuario
    return redirect('login')  # Redirigir a la página principal