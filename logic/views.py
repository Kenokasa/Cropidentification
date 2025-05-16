# views.py

import os
import json
import tempfile
import traceback
import requests

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import CropDisease, PlantScan, PlantPart, SolidWorksFile
from .forms import PlantScanForm

# Hugging Face API constants
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
HUGGINGFACE_API_TOKEN = settings.HF_API_TOKEN


# ------------------- Web Page Views -------------------

def robot_homepage(request):
    """Render robot detection homepage."""
    context = {
        'title': 'Crop Disease Detection',
        'creator': 'Mintesinot Kasa',
        'slogan': (
            'Where Artificial Intelligence meets Precision Engineering - '
            'Revolutionizing mechanical design through advanced 3D modeling '
            'and machine learning algorithms that bring robotic visions to life.'
        )
    }
    return render(request, 'home.html', context)


def view_model(request, file_id):
    """Render SolidWorks 3D model view page."""
    sw_file = get_object_or_404(SolidWorksFile, id=file_id)
    return render(request, 'viewer.html', {'file': sw_file})


class DiseaseListView(ListView):
    """Display list of known crop diseases."""
    model = CropDisease
    template_name = 'disease_list.html'
    context_object_name = 'diseases'
    paginate_by = 9


class DiseaseDetailView(DetailView):
    """Display details about a specific crop disease."""
    model = CropDisease
    template_name = 'disease_detail.html'
    context_object_name = 'disease'


# ------------------- Snapshot Saving -------------------

@csrf_exempt
def save_snapshot(request):
    """Save snapshot image and prediction results into database."""
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            detections = json.loads(request.POST['detections'])

            scan = PlantScan.objects.create(
                image=image,
                detection_data=detections,
                scan_type='CAM'
            )

            return JsonResponse({
                'status': 'success',
                'scan_id': scan.id,
                'analysis_url': reverse('scan-analysis', args=[scan.id])
            })
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# ------------------- Scan Form Processing -------------------

def scan_analysis_view(request):
    """Handle form submission to analyze uploaded plant image."""
    if request.method == 'POST':
        form = PlantScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            if request.user.is_authenticated:
                scan.user = request.user

            # Placeholder ML analysis (can replace with actual model logic)
            scan.result = analyze_image(scan.image)
            scan.save()

            return render(request, 'scan_result.html', {'scan': scan})
    else:
        form = PlantScanForm()

    return render(request, 'scan.html', {'form': form})


def analyze_image(image):
    """Placeholder function to simulate prediction. Returns dummy CropDisease."""
    return CropDisease.objects.first()


# ------------------- Hugging Face API Integration -------------------

@csrf_exempt
def predict_with_hf_model(request):
    """Receive image and return prediction using Hugging Face API."""
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({'error': 'No image file provided.'}, status=400)

            image_file = request.FILES['image']

            # Save image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                image_path = tmp.name

            # Send image to Hugging Face API
            with open(image_path, "rb") as f:
                response = requests.post(
                    HUGGINGFACE_API_URL,
                    headers={
                        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
                        "Accept": "application/json"
                    },
                    data=f.read()
                )

            os.remove(image_path)

            if response.status_code == 200:
                predictions = response.json()
                return JsonResponse({'result': predictions})
            else:
                return JsonResponse({
                    'error': 'Hugging Face request failed',
                    'details': response.json()
                }, status=response.status_code)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
