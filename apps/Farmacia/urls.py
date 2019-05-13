
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path("", views.FarmaciaIndex, name="farmacia_index"),
    
     #############################################################################################################
    # URLS Para los Presentacion de usuarios
    
    #juanjo listar usuarios tipo vendedores
    path('user/list', views.UserListView, name='user_list'),
    #juanjo listar usuarios tipo bodegueros
    path('user/listt', views.UserListView2, name='user2_list'),
    #juanjo crear usuarios
    path("user/new", views.UserCreate, name="user_create"),
    #detalle usuarios
     path('user/edit/', views. PasswordChangeView.as_view(), name="edit_pass"),
   
    path('user/info/<int:pk>', views.UserDetail.as_view(), name="user_detail"),
    #delete usuarios
     path('user/delete/<int:pk>', views.UserDelete.as_view(), name="user_delete"),
    #############################################################################################################
    # URLS Para los Medicamentos
    # Listar Tipos de Medicamentos
    path("medicamento/list", views.MedicamentoList.as_view(), name="medicamento_list"),
    # Detalle de Medicamento
    path("medicamento/info/<int:pk>", views.MedicamentoDetail.as_view(), name="medicamento_detail"),
    # Crear Tipo de Medicamento
    path("medicamento/new", views.MedicamentoCreate.as_view(), name="medicamento_create"),
    # Editar Tipo de Medicamento
    path("medicamento/edit/<int:pk>", views.MedicamentoUpdate.as_view(), name="medicamento_update"),
    # Eliminar Tipo de Medicamento
    path("medicamento/delete/<int:pk>", views.MedicamentoDelete.as_view(), name="medicamento_delete"),

    #############################################################################################################
    # Listar Tipos de Medicamentos
    path("tipo-medicamentos/list", views.TipoMedicamentoList.as_view(), name="tipo_medicamentos_list"),
    # Crear Tipo de Medicamento
    path("tipo-medicamentos/new", views.TipoMedicamentoCreate.as_view(), name="tipo_medicamentos_create"),
    # Editar Tipo de Medicamento
    path("tipo-medicamentos/edit/<int:pk>", views.TipoMedicamentoUpdate.as_view(), name="tipo_medicamentos_update"),
    # Eliminar Tipo de Medicamento
    path("tipo-medicamentos/delete/<int:pk>", views.TipoMedicamentoDelete.as_view(), name="tipo_medicamentos_delete"),
    #############################################################################################################
    # URLS Para los Presentacion de Medicamentos
    # Listar Presentacion de Medicamentos
    
    path("presentacion/list", views.PresentacionList.as_view(), name="presentacion_list"),
    # Crear Presentacion de Medicamento
    path("presentacion/new", views.PresentacionNew.as_view(), name="presentacion_new"),
    # Editar Presentacion de Medicamento
    path("presentacion/edit/<int:pk>", views.PresentacionUpdate.as_view(), name="presentacion_update"),
    # Eliminar Presentacion de Medicamento
    path("presentacion/delete/<int:pk>", views.PresentacionDelete.as_view(), name="presentacion_delete"),

    
    # URLS para proceso de Venta de Medicamentos
    path('venta/', views.VentaTemplate.as_view(), name='venta'),
    path('api/obtener_medicamentos', views.obtener_medicamentos, name="api_obtener_medicamentos"),
    path('api/seleccionar_medicamento', views.seleccionar_medicamento, name="api_seleccionar_medicamento"),

]