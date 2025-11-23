from django.urls import reverse

# Test URL
try:
    url = reverse('historiales:lista_mascota', args=[8])
    print(f"URL generada: {url}")
except Exception as e:
    print(f"Error: {e}")
