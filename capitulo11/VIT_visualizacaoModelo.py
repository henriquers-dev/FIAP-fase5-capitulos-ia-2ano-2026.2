import matplotlib.pyplot as plt
import torch
import numpy as np

# Label mapping
id2label = {0: "cat", 1: "dog"}
label2id = {v: k for k, v in id2label.items()}

# função de predição
def predict_images(model, image_processor, dataset, n_images=8):
    model.eval()
    images = []
    true_labels = []
    preds = []
    probs = []

    # model's device
    device = next(model.parameters()).device
    model.to(device) # garantir que o modelo está no device correto(gpu ou cpu)

    for i in range(n_images):
        example = dataset[i]
        image = example["image"].convert("RGB")
        label = example["labels"]

        inputs = image_processor(image, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            prob = torch.softmax(logits, dim=-1)
            pred = torch.argmax(prob, dim=-1).item()

        images.append(image)
        true_labels.append(label)
        preds.append(pred)
        probs.append(prob.max().item())

    return images, true_labels, preds, probs


# rodando as predições
images, y_true, y_pred, confidences = predict_images(
    model,
    image_processor,
    dataset["train"],
    n_images=8
)

# Plot predictions
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, ax in enumerate(axes):
    ax.imshow(images[i])
    ax.axis("off")
    ax.set_title(
        f"True: {id2label[y_true[i]]}\n"
        f"Pred: {id2label[y_pred[i]]} ({confidences[i]:.2f})",
        color="green" if y_true[i] == y_pred[i] else "red"
    )

plt.tight_layout()
plt.show()
