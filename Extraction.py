import easyocr
import json

# Fonction pour convertir les types de données non JSON-sérialisables
def convert(o):
    if isinstance(o, (numpy.int64, numpy.float64)):
        return o.item()
    raise TypeError

# Charger l'image
image_path = '/Users/achrafkhairoun/Desktop/eOnsight - Stage 2024 - Exercice technique - OCR/Genova.png'
reader = easyocr.Reader(['en'])

# Effectuer l'OCR
results = reader.readtext(image_path)

# Initialiser le résultat final
extracted_data = []
confidence_threshold = 50  # Seuil de confiance ajusté à 50%

# Parcourir les résultats et extraire les informations nécessaires
for (bbox, text, confidence) in results:
    if confidence * 100 >= confidence_threshold:
        text_info = {
            "text": text,
            "location": {
                "bbox": [[int(coord) for coord in point] for point in bbox]  # Assurez-vous que les coordonnées sont des entiers
            },
            "confidence": float(confidence) * 100  # Convertir en pourcentage et s'assurer que c'est un float
        }
        extracted_data.append(text_info)

# Sauvegarder les résultats en format JSON
output_path = '/Users/achrafkhairoun/Desktop/eOnsight - Stage 2024 - Exercice technique - OCR/extracted_data_easyocr.json'
with open(output_path, 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4, default=convert)

print(f"Results saved to {output_path}")
