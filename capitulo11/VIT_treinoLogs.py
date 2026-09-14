import pandas as pd

logs = pd.DataFrame(trainer.state.log_history)


train_logs = logs[logs["loss"].notna()][["epoch", "loss"]]
eval_logs = logs[logs["eval_loss"].notna()][["epoch", "eval_loss"]]


plt.figure(figsize=(10, 6))

plt.plot(train_logs["epoch"], train_logs["loss"], marker="o", label="Training Loss")
plt.plot(eval_logs["epoch"], eval_logs["eval_loss"], marker="o", label="Evaluation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training & Evaluation Loss per Epoch")
plt.legend()
plt.grid(True)
plt.show()
