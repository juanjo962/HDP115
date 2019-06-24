from django import forms
from .models import TipoMedicamento, Medicamento, Presentacion

# Crear Formularios aqui
#Formulario para los TIPOS DE MEDICAMENTOS  
class TipoMedicamentoForm(forms.ModelForm):
    class Meta():
        model = TipoMedicamento
        fields = ['tipo',]
        labels = {
            'tipo': "Ingrese el Tipo de Medicamento (Por su uso o efectos secundarios):"
        }
        widgets = {
            'tipo': forms.TextInput(attrs={"class": "form-control", "required": True})
        }


# formulario  para las PRESENTACIONES DE MEDICAMENTOS    ##################################################
class PresentacionForm(forms.ModelForm):
    class Meta():
        model = Presentacion
        fields = ['presentacion',]
        labels = {
            'presentacion': "Ingrese la Presentacion del Medicamento:"
        }
        widgets = {
            'presentacion': forms.TextInput(attrs={"class": "form-control", "required": True})
        }
class MedicamentoForm(forms.ModelForm):
    class Meta():
        model = Medicamento
        fields = ['id_presentacion', 'id_tipo', 'nombre', 'precio','existencia']
        labels = {
            'id_presentacion': "Presentacion del Medicamento",
            'id_tipo': "Tipo de Medicamento",
            'nombre': "Nombre del Medicamento",
            'precio': "Precio del Medicamento",
            'existencia': "Existencia del Medicamento",
        }
        widgets = {
            'id_presentacion': forms.Select(choices=Presentacion.objects.all(), attrs={"class": "form-control", "required": True}),
            'id_tipo': forms.Select(choices=TipoMedicamento.objects.all(), attrs={"class": "form-control", "required": True}),
            'nombre': forms.TextInput(attrs={"class": "form-control", "required": True}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'value': '0', "type": "number", "min": 0, "step":".01", "lang": "en"}),
            'existencia': forms.TextInput(attrs={'class': 'form-control',"step":1,"type": "number", "min": 0}),

        }