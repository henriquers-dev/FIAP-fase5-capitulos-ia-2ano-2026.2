import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dados_sensor.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df_rotulado = pd.DataFrame()
clicks = []

def on_click(event):
    if event.dblclick:
        time_clicked = pd.to_datetime(event.xdata, unit="s")
        clicks.append(time_clicked)
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(12, 8))
axs[0].plot(df["timestamp"], df["ax"], label="Accel X")
axs[1].plot(df["timestamp"], df["ay"], label="Accel Y", color="orange")
axs[2].plot(df["timestamp"], df["az"], label="Accel Z", color="green")

axs[0].legend()
axs[1].legend()
axs[2].legend()

plt.xlabel("Tempo")

fig.suptitle("Duplos cliques sequenciais: Repouso → Movimento → Repouso...", fontsize=14)
fig.canvas.mpl_connect("button_press_event", on_click)
plt.show()

i = 0
bloco = 0

while i < len(clicks):
    t0 = clicks[i]
    bloco_df = df[df["timestamp"] >= t0].head(20).copy()
    label = "repouso" if bloco % 2 == 0 else "movimento"
    bloco_df["label"] = label
    df_rotulado = pd.concat([df_rotulado, bloco_df], ignore_index=True)
    i += 1
    bloco += 1

df_rotulado.to_csv("dados_rotulados.csv", index=False)
print("Arquivo salvo como dados_rotulados.csv com blocos de 20 linhas rotuladas sequencialmente.")
