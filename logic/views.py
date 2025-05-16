from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import CropDisease, PlantScan, PlantPart
from .forms import PlantScanForm
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PlantScan

from django.shortcuts import render
# views.py
from django.shortcuts import render
from .models import SolidWorksFile

def view_model(request, file_id):
    sw_file = SolidWorksFile.objects.get(id=file_id)
    return render(request, 'viewer.html', {'file': sw_file})
def robot_homepage(request):
    """View to render the mechanical robot frontend"""
    context = {
        'title': 'Crop Disease Ditection',
        'creator': 'Mintesinot Kasa',
        'slogan': 'Where Artificial Intelligence meets Precision Engineering - '
                 'Revolutionizing mechanical design through advanced 3D modeling '
                 'and machine learning algorithms that bring robotic visions to life.'
    }
    return render(request, 'home.html', context)

def save_snapshot(request):
    if request.method == 'POST':
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
    return JsonResponse({'status': 'error'}, status=400)
class DiseaseListView(ListView):
    model = CropDisease
    template_name = 'disease_list.html'
    context_object_name = 'diseases'
    paginate_by = 9

class DiseaseDetailView(DetailView):
    model = CropDisease
    template_name = 'disease_detail.html'
    context_object_name = 'disease'

def scan_analysis_view(request):
    if request.method == 'POST':
        form = PlantScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            if request.user.is_authenticated:
                scan.user = request.user

            # Add ML model analysis here
            scan.result = analyze_image(scan.image)  # Replace with your ML model
            scan.save()

            return render(request, 'scan_result.html', {'scan': scan})
    else:
        form = PlantScanForm()
    return render(request, 'scan.html', {'form': form})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from gradio_client import Client
import tempfile
import os
import traceback

def predict(request):
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({"error": "No image file provided."}, status=400)

            image_file = request.FILES['image']

            # Save uploaded image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Call Hugging Face Space prediction
            try:
                client = Client("https://jarif-crop-disease-identification.hf.space/--replicas/frp3j/")
                result = client.predict(
                    tmp_path,     # Pass local file path to HF API
                    api_name="/predict"
                )
            finally:
                os.remove(tmp_path)

            return JsonResponse({"result": result}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": f"Prediction failed: {str(e)}"}, status=500)

    return JsonResponse({"error": "POST request with an image file is required."}, status=400)

# def plant_part_api(request, identifier):
#     try:
#         part = PlantPart.objects.get(model_identifier=identifier)
#         data = {
#             'name': part.name,
#             'description': part.description,
#             'diseases': [{
#                 'name': d.name,
#                 'url': d.get_absolute_url()
#             } for d in part.common_diseases.all()]
#         }
#         return JsonResponse(data)
#     except PlantPart.DoesNotExist:
#         return JsonResponse({'error': 'Part not found'}, status=404)

# def analyze_image(image):
#     # Placeholder for your ML model integration
#     # This should return a CropDisease instance
#     return CropDisease.objects.first()
