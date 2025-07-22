from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
import requests  # For interacting with the API

# Static Disease Mapping
DISEASE_MAPPING = {
    0: {
        "name": "Acne and Rosacea Photos",
        "common_name": "Acne",
        "symptoms": ["Red spots", "Pimples", "Blackheads", "Inflamed skin"],
        "precautions": ["Keep your skin clean", "Use non-comedogenic products", "Avoid touching your face", "Consult a dermatologist if severe"],
    },
    1: {
        "name": "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions",
        "common_name": "Pre-cancerous Skin Lesions",
        "symptoms": ["Scaly patches", "Crusty skin", "Rough texture", "Itching or burning sensation"],
        "precautions": ["Use sunscreen with high SPF", "Avoid direct sunlight", "Wear protective clothing outdoors", "Regularly check for skin changes"],
    },
    2: {
        "name": "Atopic Dermatitis Photos",
        "common_name": "Eczema",
        "symptoms": ["Dry skin", "Itchy patches", "Red, inflamed skin", "Cracked or scaly areas"],
        "precautions": ["Moisturize daily", "Avoid harsh soaps", "Stay hydrated", "Avoid scratching"],
    },
    4: {
        "name": "Bullous Disease Photos",
        "common_name": "Blistering Skin Diseases",
        "symptoms": ["Blisters on skin", "Fluid-filled lesions", "Painful sores", "Skin peeling"],
        "precautions": ["Avoid friction on skin", "Use prescribed medications", "Keep blisters clean", "Consult a specialist"],
    },
    5: {
        "name": "Cellulitis Impetigo and other Bacterial Infections",
        "common_name": "Bacterial Skin Infections",
        "symptoms": ["Red, swollen skin", "Warmth in affected area", "Pain and tenderness", "Pus or drainage"],
        "precautions": ["Keep wounds clean", "Avoid scratching", "Use prescribed antibiotics", "Seek medical care if severe"],
    },
    6: {
        "name": "Eczema Photos",
        "common_name": "Eczema",
        "symptoms": ["Dry, itchy skin", "Red patches", "Cracking or oozing skin", "Thickened skin in chronic cases"],
        "precautions": ["Use hypoallergenic moisturizers", "Avoid allergens", "Wear soft fabrics", "Apply topical treatments as prescribed"],
    },
    7: {
        "name": "Exanthems and Drug Eruptions",
        "common_name": "Rashes from Drug Reactions",
        "symptoms": ["Widespread red rashes", "Itching", "Swelling", "Fever (in some cases)"],
        "precautions": ["Avoid known drug allergens", "Consult a doctor immediately", "Take antihistamines for relief", "Discontinue the triggering medication"],
    },
    8: {
        "name": "This is healthy and normal skin",
        "common_name": "Normal Skin",
        "symptoms": ["Smooth texture", "Even skin tone", "No visible lesions", "Healthy glow"],
        "precautions": ["Maintain a balanced diet", "Stay hydrated", "Use mild skincare products", "Protect from excessive sun exposure"],
    },
    9: {
        "name": "Hair Loss Photos Alopecia and other Hair Diseases",
        "common_name": "Hair Loss",
        "symptoms": ["Thinning hair", "Bald patches", "Excessive hair fall", "Scalp irritation"],
        "precautions": ["Avoid tight hairstyles", "Eat a nutrient-rich diet", "Use gentle hair care products", "Consult a trichologist"],
    },
    10: {
        "name": "Herpes HPV and other STDs Photos",
        "common_name": "Sexually Transmitted Skin Infections",
        "symptoms": ["Blisters in affected areas", "Itching or burning sensation", "Sores or ulcers", "Skin redness"],
        "precautions": ["Practice safe sex", "Avoid direct contact with sores", "Seek medical advice", "Use antiviral treatments"],
    },
    11: {
        "name": "Light Diseases and Disorders of Pigmentation",
        "common_name": "Pigmentation Disorders",
        "symptoms": ["Light or dark patches", "Uneven skin tone", "Sensitivity to sunlight", "Skin discoloration"],
        "precautions": ["Use sunscreen", "Avoid harsh chemicals", "Consult a dermatologist for treatments", "Stay hydrated"],
    },
    12: {
        "name": "Lupus and other Connective Tissue diseases",
        "common_name": "Lupus Skin Disease",
        "symptoms": ["Butterfly-shaped rash on face", "Sensitivity to sunlight", "Inflamed skin patches", "Fatigue"],
        "precautions": ["Avoid prolonged sun exposure", "Use protective clothing", "Follow prescribed medications", "Monitor symptoms regularly"],
    },
    14: {
        "name": "Melanoma Skin Cancer Nevi and Moles",
        "common_name": "Skin Cancer",
        "symptoms": ["New or changing moles", "Asymmetrical lesions", "Irregular borders", "Dark pigmentation"],
        "precautions": ["Regular skin checks", "Avoid tanning beds", "Use sunscreen daily", "Consult an oncologist for abnormal moles"],
    },
    15: {
        "name": "Nail Fungus and other Nail Disease",
        "common_name": "Nail Fungus",
        "symptoms": ["Discolored nails", "Thickened nails", "Brittle or cracked nails", "Pain around the nails"],
        "precautions": ["Keep nails dry and clean", "Avoid sharing nail tools", "Use antifungal treatments", "Wear breathable footwear"],
    },
    16: {
        "name": "Poison Ivy Photos and other Contact Dermatitis",
        "common_name": "Allergic Skin Reaction",
        "symptoms": ["Red rashes", "Blisters", "Severe itching", "Swelling in affected areas"],
        "precautions": ["Avoid contact with allergens", "Wash skin immediately after exposure", "Use topical corticosteroids", "Take antihistamines for relief"],
    },
    17: {
        "name": "Psoriasis pictures Lichen Planus and related diseases",
        "common_name": "Psoriasis",
        "symptoms": ["Scaly, red patches", "Dry and cracked skin", "Itching or burning sensation", "Thickened nails"],
        "precautions": ["Keep skin moisturized", "Avoid triggers like stress", "Follow prescribed treatments", "Expose skin to natural sunlight moderately"],
    },
    18: {
        "name": "Scabies Lyme Disease and other Infestations and Bites",
        "common_name": "Scabies",
        "symptoms": ["Intense itching", "Red rashes", "Tiny burrow marks on skin", "Irritated skin"],
        "precautions": ["Avoid close contact with infected individuals", "Wash clothing and bedding in hot water", "Use prescribed creams", "Maintain hygiene"],
    },
    19: {
        "name": "Seborrheic Keratoses and other Benign Tumors",
        "common_name": "Benign Skin Growths",
        "symptoms": ["Waxy or wart-like growths", "Skin discoloration", "Non-painful lesions", "Flat or raised bumps"],
        "precautions": ["Avoid scratching", "Keep skin moisturized", "Consult a dermatologist if growths change", "Protect skin from UV rays"],
    },
    20: {
        "name": "Systemic Disease",
        "common_name": "Systemic Skin Conditions",
        "symptoms": ["Skin rashes", "Fatigue", "Fever", "Swollen lymph nodes"],
        "precautions": ["Follow prescribed medications", "Monitor systemic symptoms", "Maintain a healthy lifestyle", "Consult a specialist for diagnosis"],
    },
    21: {
        "name": "Tinea Ringworm Candidiasis and other Fungal Infections",
        "common_name": "Fungal Infections",
        "symptoms": ["Circular red rashes", "Itching or burning sensation", "Scaling skin", "Cracked or peeling skin"],
        "precautions": ["Keep affected areas dry", "Avoid sharing personal items", "Use antifungal medications", "Wear loose, breathable clothing"],
    },
    22: {
        "name": "Urticaria Hives",
        "common_name": "Hives",
        "symptoms": ["Raised, red welts", "Severe itching", "Swelling", "Skin irritation"],
        "precautions": ["Avoid allergens", "Use antihistamines", "Keep skin cool", "Avoid tight clothing"],
    },
    23: {
        "name": "Vascular Tumors",
        "common_name": "Skin Vascular Tumors",
        "symptoms": ["Red or purple lesions", "Swelling", "Visible blood vessels", "Pain in some cases"],
        "precautions": ["Avoid skin trauma", "Protect skin from UV rays", "Consult a specialist", "Monitor changes in lesions"],
    },
    24: {
        "name": "Vasculitis Photos",
        "common_name": "Vasculitis",
        "symptoms": ["Red patches or rashes", "Painful sores", "Swollen skin", "Fatigue"],
        "precautions": ["Avoid allergens", "Follow prescribed treatments", "Maintain a healthy diet", "Consult a doctor for monitoring"],
    },
}


def symptom_checker(request):
    return render(request, 'symptom_checker/symptom_checker.html')

def symptom_checker_results(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Save the uploaded image
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Prepare the image for the API request
        api_url = "https://74gz61cs-8000.euw.devtunnels.ms/predict/"
        files = {'image': image.file}  # Send image as form-data

        try:
            # Send the image to the API
            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                # Parse the API response
                data = response.json()
                predicted_class = data.get('predicted_class', None)
                print(response.json())

                # Fetch disease details
                disease_info = DISEASE_MAPPING.get(predicted_class, None)
                if disease_info:
                    predictions = {
                        "class_id": predicted_class,
                        "disease_name": disease_info["name"],
                        "common_name": disease_info["common_name"],
                        "symptoms": disease_info["symptoms"],
                        "precautions": disease_info["precautions"],
                    }
                else:
                    predictions = {"disease_name": "Unknown", "common_name": "Unknown", "symptoms": [], "precautions": []}

                # Recommended doctors and articles (can be dynamically fetched)
                recommended_doctors = [
                    {"name": "Dr. Sarah Khan", "specialization": "Dermatologist", "location": "Lahore"},
                    {"name": "Dr. Umar Gujjar", "specialization": "Skin Specialist", "location": "Islamabad"},
                ]
                related_articles = [
                    {"title": "Understanding Acne", "url": "/articles/acne"},
                    {"title": "Managing Skin Conditions", "url": "/articles/skin-care"},
                ]

                return render(request, 'symptom_checker/symptom_result.html', {
                    'uploaded_file_url': uploaded_file_url,
                    'predictions': predictions,
                    'recommended_doctors': recommended_doctors,
                    'related_articles': related_articles
                })

            else:
                # API error handling
                return render(request, 'symptom_checker/symptom_result.html', {
                    'error': 'Failed to fetch predictions. Please try again later.',
                })

        except requests.exceptions.RequestException as e:
            # Handle API connection errors
            print(f"Error connecting to the API: {e}")
            return render(request, 'symptom_checker/symptom_result.html', {
                'error': 'Error connecting to the prediction API. Please try again later.',
            })

    return render(request, 'symptom_checker/symptom_result.html', {'error': 'No image uploaded.'})

# PDF Generation Function
def generate_pdf_report(request, predicted_class):
    # Fetch disease info
    disease_info = DISEASE_MAPPING.get(predicted_class, {})
    user_name = request.user.get_full_name() if request.user.is_authenticated else "Guest User"
    user_email = request.user.email if request.user.is_authenticated else "guest@example.com"

    context = {
        "company_logo": "/static/images/logo.png",
        "user_name": user_name,
        "user_email": user_email,
        "user_age": "Unknown",
        "user_blood_group": "Unknown",
        "uploaded_image": "/media/uploaded_image.jpg",  # Replace dynamically
        "disease_name": disease_info.get("name", "Unknown"),
        "disease_common_name": disease_info.get("common_name", "Unknown"),
        "disease_symptoms": disease_info.get("symptoms", []),
        "disease_precautions": disease_info.get("precautions", []),
    }

    # Render the PDF
    template = get_template("report_template.html")
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    return HttpResponse("Error generating PDF")
