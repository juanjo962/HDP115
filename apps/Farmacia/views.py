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
FIRST_NAME="Jose"
LAST_NAME="Gonzalez"

if User.objects.filter(username=USER).count()==0:
    if User.objects.filter(is_superuser=1).count()==0:
        superuser=User.objects.create_superuser(username=USER,email=MAIL,password=PASS,first_name=FIRST_NAME,last_name=LAST_NAME)
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


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = "user/user_list.html"
    context_object_name = "users"
################################

########################################
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
@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
    model = User
    template_name = "user/user_detail.html"
    context_object_name = "users"

#JUANJO:borrar usuario
@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class VentaTemplate(TemplateView):
    template_name = 'facturacion/factura.html'

@method_decorator(login_required, name='dispatch')
def obtener_medicamentos(request):
    meds = Medicamento.objects.all().values()
    meds_list = list(meds)
    return JsonResponse(meds_list, safe=False)

@method_decorator(login_required, name='dispatch')
def seleccionar_medicamento(request):
    id = request.GET.get('id', None)
    med = Medicamento.objects.filter(id_medicamento=id).values()
    med_list = list(med)
    return JsonResponse(med_list, safe=False)

#######################################################################################
# Vistas para el CRUD de Medicamentos
# Acciones: Crear, Actualizar, Eliminar, Listar, Detalles
@method_decorator(login_required, name='dispatch')
class MedicamentoList(ListView):
    model = Medicamento
    template_name = "medicamento/medicamento_list.html"
    context_object_name = "medicamentos"
    paginate_by = 10
    

@method_decorator(login_required, name='dispatch')
class MedicamentoDetail(DetailView):
    model = Medicamento
    template_name = "medicamento/medicamento_detail.html"
    context_object_name = "medicamento"

@method_decorator(login_required, name='dispatch')
class MedicamentoCreate(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_new.html"

@method_decorator(login_required, name='dispatch')
class MedicamentoUpdate(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_update.html"

@method_decorator(login_required, name='dispatch')
class MedicamentoDelete(DeleteView):
    model = Medicamento
    success_url = reverse_lazy("medicamento_list")
    template_name = "medicamento/medicamento_delete.html"
    context_object_name = "medicamento"

    ###INVENTARIO XD
    
@method_decorator(login_required, name='dispatch')
class InventarioList(ListView):
    model = Medicamento
    template_name = "Inventario/Inventario_list.html"
    context_object_name = "medicamentos"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class InventarioDetail(DetailView):
    model = Medicamento
    template_name = "Inventario/Inventario_detail.html"
    context_object_name = "medicamento"


@method_decorator(login_required, name='dispatch')
class InventarioCreate(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_new.html"


@method_decorator(login_required, name='dispatch')
class InventarioUpdate(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_update.html"


@method_decorator(login_required, name='dispatch')
class InventarioDelete(DeleteView):
    model = Medicamento
    success_url = reverse_lazy("Inventario_list")
    template_name = "Inventario/Inventario_delete.html"
    context_object_name = "medicamento"
    



###TIPO MEDICAMENTO
@method_decorator(login_required, name='dispatch')
class TipoMedicamentoList(ListView):
    model = TipoMedicamento #recordar importar modelo de TipoMedicamento
    template_name = "tipo_medicamento/tipo_medicamento_list.html"
    context_object_name = "tipo_medicamentos"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class TipoMedicamentoCreate(CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_new.html"


@method_decorator(login_required, name='dispatch')
class TipoMedicamentoUpdate(UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_update.html"


@method_decorator(login_required, name='dispatch')
class TipoMedicamentoDelete(DeleteView):
    model = TipoMedicamento
    success_url = reverse_lazy("tipo_medicamentos_list")
    template_name = "tipo_medicamento/tipo_medicamento_delete.html"
    context_object_name = "tipo_medicamentos"

#######################################################################################
# Vistas para el CRUD de PRESENTACIONES
# Acciones: Crear, Actualizar, Eliminar, Listar


@method_decorator(login_required, name='dispatch')
class PresentacionList(ListView):
    model = Presentacion #recordar importar modelo de presentacion
    template_name = "presentacion/presentacion_list.html"
    context_object_name = "presentaciones"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class PresentacionNew(CreateView):
    model = Presentacion
    form_class = PresentacionForm
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_new.html"


@method_decorator(login_required, name='dispatch')
class PresentacionUpdate(UpdateView):
    model = Presentacion
    form_class = PresentacionForm
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_update.html"


@method_decorator(login_required, name='dispatch')
class PresentacionDelete(DeleteView):
    model = Presentacion
    success_url = reverse_lazy("presentacion_list")
    template_name = "presentacion/presentacion_delete.html"
    context_object_name = "presentacion"











