from django.urls import path
from . import views  # Assure-toi d'importer les vues

urlpatterns = [
    path('', views.prediction_view, name='home'),  # Route pour afficher le formulaire de prédiction
    path('predict/', views.prediction_view, name='predict'),  # Route pour la prédiction
]
