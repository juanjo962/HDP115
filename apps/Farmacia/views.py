from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.views import PasswordResetView,LoginView
from django.shortcuts import render, redirect,render_to_response

from django.urls import reverse_lazy,reverse


# Import de Vistas Basadas en Clase para los CRUD basicos
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import de Formularios
from .forms import TipoMedicamentoForm, MedicamentoForm, PresentacionForm
# Import de Modelos
from .models import TipoMedicamento, Medicamento, Presentacion,Venta, User,Rol
# Import de Herramientas para Ajax
import json
from django.http import JsonResponse, HttpResponse

#import form
from apps.usuarios.forms import SignUpForm
from apps.usuarios.views import sign_up
#import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.



USER="admin"
PASS="123456"
MAIL="admin@gmail.com"
if User.objects.filter(username=USER).count()==0:
    if User.objects.filter(is_superuser=1).count()==0:
        superuser=User.objects.create_superuser(username=USER,email=MAIL,password=PASS)
        superuser.save()


def FarmaciaIndex(request):
    if  request.user.is_authenticated:
        medicamentos =Medicamento.objects.count()
        empleados = User.objects.count()
        return render(request,'farmacia/farmacia.html',
        {
            """'compras' : compras, 
            'ventas' : ventas,"""
            'medicamentos' : medicamentos,
            'empleados' : empleados
        })
    else:
        return redirect('login')
       
#######################################################################################
# Vistas para el CRUD de usuarios
# Acciones: Crear,cambiar pass , Eliminar, Listar, Detalles

#JUANJO: clase para listar los vendedores
def UserListView(request):
    queryse= User.objects.filter(id_rol=2)
    contexto={'users':queryse}
    return render(request,'user/user_list.html',contexto)

#JUANJO: clase para listar los administradores
def UserListView2(request):
    queryse= User.objects.filter(id_rol=1)
    contexto={'users':queryse}
    return render(request,'user/user2_list.html',contexto)

#JUANJO:crear nuevo usuario
def UserCreate(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # form.id_rol.queryset=Rol.objects.filter(id_rol=[3,4])
        if form.is_valid():
            # Guardamos el Usuario
            form.save()
            return redirect('user_list')
    else:
        form = SignUpForm()
        # redirigir el formulario vacio para llenar los datos
    return render(request,'user/user_create.html',{'form':form})

#JUANJO:detalle de usuario
class UserDetail(DetailView):
    model = User
    template_name = "user/user_detail.html"
    context_object_name = "users"

#JUANJO:borrar usuario
class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy("user_list")
    template_name = "user/user_delete.html"
    context_object_name = "users"

#JUANJO:cambia contraseña por usuario
class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("farmacia_index")
    template_name = "user/user_update.html"
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class VentaTemplate(TemplateView):
    template_name = 'facturacion/factura.html'

def obtener_medicamentos(request):
    meds = Medicamento.objects.all().values()
    meds_list = list(meds)
    return JsonResponse(meds_list, safe=False)

def seleccionar_medicamento(request):
    id = request.GET.get('id', None)
    med = Medicamento.objects.filter(id_medicamento=id).values()
    med_list = list(med)
    return JsonResponse(med_list, safe=False)

#######################################################################################
# Vistas para el CRUD de Medicamentos
# Acciones: Crear, Actualizar, Eliminar, Listar, Detalles
class MedicamentoList(ListView):
    model = Medicamento
    template_name = "medicamento/medicamento_list.html"
    context_object_name = "medicamentos"
    paginate_by = 10

class MedicamentoDetail(DetailView):
    model = Medicamento
    template_name = "medicamento/medicamento_detail.html"
    context_object_name = "medicamento"

class MedicamentoCreate(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_new.html"

class MedicamentoUpdate(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_update.html"

class MedicamentoDelete(DeleteView):
    model = Medicamento
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_delete.html"
    context_object_name = "medicamento"

    ###INVENTARIO XD
class InventarioList(ListView):
    model = Medicamento
    template_name = "Inventario/Inventario_list.html"
    context_object_name = "medicamentos"
    paginate_by = 10

class InventarioDetail(DetailView):
    model = Medicamento
    template_name = "Inventario/Inventario_detail.html"
    context_object_name = "medicamento"

class InventarioCreate(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_new.html"

class InventarioUpdate(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_update.html"

class InventarioDelete(DeleteView):
    model = Medicamento
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_delete.html"
    context_object_name = "medicamento"
    



###TIPO MEDICAMENTO
class TipoMedicamentoList(ListView):
    model = TipoMedicamento #recordar importar modelo de TipoMedicamento
    template_name = "tipo_medicamento/tipo_medicamento_list.html"
    context_object_name = "tipo_medicamentos"
    paginate_by = 10

class TipoMedicamentoCreate(CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_new.html"

class TipoMedicamentoUpdate(UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_update.html"

class TipoMedicamentoDelete(DeleteView):
    model = TipoMedicamento
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_delete.html"
    context_object_name = "tipo_medicamentos"

#######################################################################################
# Vistas para el CRUD de PRESENTACIONES
# Acciones: Crear, Actualizar, Eliminar, Listar

class PresentacionList(ListView):
    model = Presentacion #recordar importar modelo de presentacion
    template_name = "presentacion/presentacion_list.html"
    context_object_name = "presentaciones"
    paginate_by = 10

class PresentacionNew(CreateView):
    model = Presentacion
    form_class = PresentacionForm
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_new.html"

class PresentacionUpdate(UpdateView):
    model = Presentacion
    form_class = PresentacionForm
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_update.html"

class PresentacionDelete(DeleteView):
    model = Presentacion
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_delete.html"
    context_object_name = "presentacion"













