from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import torch

# 1. Carregar imagem (exemplo: local ou URL)
img = Image.open("carro-completo.jpeg").convert("RGB")

# 2. Preparar imagem com o feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
inputs = feature_extractor(images=img, return_tensors="pt")

# 3. Carregar modelo pré-treinado
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
model.eval()

# 4. Inferência
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

print("Classe prevista:", model.config.id2label[predicted_class_idx])
