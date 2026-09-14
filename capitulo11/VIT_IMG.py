# fine tune
from datasets import load_dataset
from transformers import ViTImageProcessor, ViTForImageClassification, TrainingArguments, Trainer
import numpy as np
import torch

# 1. Carregar dataset — por exemplo, cats_vs_dogs
dataset = load_dataset("microsoft/cats_vs_dogs")  # exemplo de dataset público

# 2. Pré-processamento: redimensionar, normalizar imagens
image_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')

def preprocess_function(examples):
    # 'examples' will be a dictionary of lists if batched=True
    # Each item in examples['image'] is a PIL Image object
    images = [img.convert("RGB") for img in examples['image']]
    # image_processor returns a dict with 'pixel_values'
    inputs = image_processor(images=images, return_tensors="pt")
    inputs['labels'] = examples['labels']
    return inputs

# Apply preprocessing with .map
processed_dataset = dataset.map(preprocess_function, batched=True)
# Remove original columns not needed by the model
processed_dataset = processed_dataset.remove_columns(['image'])

# 3. Carregar modelo pré-treinado (com cabeçalho para classificação)
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224', num_labels=2, ignore_mismatched_sizes=True)

# 4. Configurar treinamento
training_args = TrainingArguments(
    output_dir="./vit-finetuned-cats-dogs",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    learning_rate=5e-5,
    report_to=[]
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=processed_dataset["train"].shuffle(seed=42).select(range(2000)),  # exemplo reduzido
    eval_dataset=processed_dataset["train"].shuffle(seed=42).select(range(2000,2500)), # Using part of train for eval, as only 'train' split was available
)

# 5. Treinar
trainer.train()
