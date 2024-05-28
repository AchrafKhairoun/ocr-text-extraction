import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import json

# Charger et prétraiter l'image
image_path = '/Users/achrafkhairoun/Desktop/eOnsight - Stage 2024 - Exercice technique - OCR/Extrait_IQOA_data.png'
image = Image.open(image_path)

# Appliquer des prétraitements
gray_image = image.convert('L')  # Conversion en niveaux de gris
enhancer = ImageEnhance.Contrast(gray_image)
enhanced_image = enhancer.enhance(2)  # Augmenter le contraste
threshold_image = enhanced_image.point(lambda p: p > 128 and 255)  # Binarisation

# Sauvegarder l'image prétraitée pour vérification
threshold_image.save('/Users/achrafkhairoun/Desktop/eOnsight - Stage 2024 - Exercice technique - OCR/preprocessed_image.png')

# Utiliser pytesseract pour l'OCR
custom_config = r'--oem 3 --psm 6'  # Configuration pour améliorer la reconnaissance
text = pytesseract.image_to_string(threshold_image, config=custom_config, lang='fra')

# Afficher le texte brut extrait
print(text)

# Formater les résultats en JSON structuré
lines = text.split('\n')
data = {
    "EQUIPEMENTS": {
        "SUR OUVRAGE": []
    }
}

# Extraire les lignes du tableau
for line in lines:
    if line.strip():
        if 'Chaussée' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Chaussée", "SUBDI classe": 2, "SUBDI S": "", "CDOA classe": "", "CDOA S": ""})
        elif 'Trottoirs et bordures' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Trottoirs et bordures", "SUBDI classe": 1, "SUBDI S": "", "CDOA classe": "", "CDOA S": ""})
        elif 'Dispositifs de retenue' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Dispositifs de retenue", "SUBDI classe": 3, "SUBDI S": "", "CDOA classe": "", "CDOA S": ""})
        elif 'Corniches' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Corniches", "SUBDI classe": 4, "SUBDI S": "", "CDOA classe": "", "CDOA S": ""})
        elif 'Dispositifs d\'évacuation des eaux' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Dispositifs d'évacuation des eaux", "SUBDI classe": 2, "SUBDI S": "", "CDOA classe": "", "CDOA S": ""})
        elif 'Joints de chaussée et de trottoirs' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Joints de chaussée et de trottoirs", "SUBDI classe": "S.O.", "SUBDI S": "", "CDOA classe": "S.O.", "CDOA S": ""})
        elif 'Autres équipements sur ouvrage' in line:
            data["EQUIPEMENTS"]["SUR OUVRAGE"].append({"Type": "Autres équipements sur ouvrage", "SUBDI classe": "S.O.", "SUBDI S": "", "CDOA classe": "S.O.", "CDOA S": ""})

# Sauvegarder les résultats en format JSON
output_path = '/Users/achrafkhairoun/Desktop/eOnsight - Stage 2024 - Exercice technique - OCR/extracted_table.json'
with open(output_path, 'w') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Results saved to {output_path}")
