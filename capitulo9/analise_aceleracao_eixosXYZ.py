import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carrega os dados do CSV
df = pd.read_csv("dados_mpu6050.csv")
# Converte o timestamp para o formato datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])
# Cria a figura com 3 subplots verticais (um para cada eixo)
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    subplot_titles=("Aceleração no eixo X", "Aceleração no eixo Y", "Aceleração no eixo Z"))
# Gráfico do eixo X
fig.add_trace(go.Scatter(x=df["timestamp"], y=df["ax"], mode='lines+markers', name="ax"),
              row=1, col=1)

# Gráfico do eixo Y
fig.add_trace(go.Scatter(x=df["timestamp"], y=df["ay"], mode='lines+markers', name="ay"),
              row=2, col=1)

# Gráfico do eixo Z
fig.add_trace(go.Scatter(x=df["timestamp"], y=df["az"], mode='lines+markers', name="az"),
              row=3, col=1)

# Configurações finais
fig.update_layout(height=600, width=900, title_text="Sinais de Aceleração nos Três Eixos",
                  hovermode="x unified")

fig.update_yaxes(title_text="ax (g)", row=1, col=1)
fig.update_yaxes(title_text="ay (g)", row=2, col=1)
fig.update_yaxes(title_text="az (g)", row=3, col=1)
fig.update_xaxes(title_text="Tempo", row=3, col=1)

fig.show()
