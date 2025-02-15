from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm

# metodo que devuelve el json

def lista_productos(request):
    productos = Producto.objects.all()
    data = [
        {
            'nombre': p.nombre,
            'precio': p.precio,
            'imagen': p.imagen,
        }
        for p in productos
    ]
    return JsonResponse(data, safe=False)

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar')
    else:
        form = ProductoForm()
    return render(request, 'agregar.html', {'form': form})