from django.shortcuts import render
from django.http import JsonResponse
from .models import FloodThreat, SocialVulnerability

# Create your views here.
def index(request):
    return render(request, 'render/index.html', {})

def healthz(request):
    return JsonResponse({'status': 'ok'})

def flood_layer(request):
    """API endpoint to get flood threat layer as GeoJSON"""
    flood_threats = FloodThreat.objects.all()
    
    # Build GeoJSON FeatureCollection manually for more control
    features = []
    for threat in flood_threats:
        features.append({
            'type': 'Feature',
            'id': threat.id,
            'properties': {
                'name': threat.name,
                'description': threat.description,
                'threat_level': threat.threat_level,
            },
            'geometry': {
                'type': threat.geometry.geom_type,
                'coordinates': threat.geometry.coords,
            }
        })
    
    geojson_data = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(geojson_data, safe=False)

def vulnerability_layer(request):
    """API endpoint to get social vulnerability layer as GeoJSON"""
    vulnerabilities = SocialVulnerability.objects.all()
    
    # Build GeoJSON FeatureCollection manually for more control
    features = []
    for vuln in vulnerabilities:
        features.append({
            'type': 'Feature',
            'id': vuln.id,
            'properties': {
                'name': vuln.name,
                'description': vuln.description,
                'vulnerability_index': vuln.vulnerability_index,
                'affected_population': vuln.affected_population,
                'linked_families': vuln.linked_families,
            },
            'geometry': {
                'type': vuln.geometry.geom_type,
                'coordinates': vuln.geometry.coords,
            }
        })
    
    geojson_data = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(geojson_data, safe=False)
