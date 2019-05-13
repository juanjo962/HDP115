from django.urls import path
# Importando vistas del modulo usuarios
from . import views

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	# Pagina principal del Sitio
	path('init/', views.index, name='kardex_index'),
	# Pagina de Registro de Usuarios
    path('signup/', views.sign_up, name='sign_up'),
    # Pagina para iniciar sesion
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # Pagina para finalizar sesion
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    #juanjo listar bodegueros

]
