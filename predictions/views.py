import requests
from django.shortcuts import render
from .forms import TextInputForm

def prediction_view(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            response = requests.post('http://127.0.0.1:8001/predict/', json={"text": text})
            prediction = response.json() if response.status_code == 200 else {'error': 'Erreur'}
            return render(request, 'result.html', {'prediction': prediction})
    else:
        form = TextInputForm()
    return render(request, 'predict.html', {'form': form})
