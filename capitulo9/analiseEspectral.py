import pandas as pd              # Para leitura e manipulação de dados tabulares
import numpy as np              # Para operações matemáticas e FFT
import matplotlib.pyplot as plt # Para geração dos gráficos

# Lê o arquivo contendo os dados do sensor (colunas: timestamp e accX)
df = pd.read_csv('dados_sensor.csv')

# Calcula o intervalo entre amostras (diferença entre timestamps consecutivos)
dts = df['timestamp'].diff().dropna()   # dropna() remove o primeiro valor NaN

# Calcula a taxa de amostragem média (1 / intervalo médio)
sampling_rate = 1 / dts.mean()

print(f"Taxa de amostragem estimada: {sampling_rate:.2f} Hz")

# Extrai os dados do eixo X como vetor NumPy
signal = df['accX'].values

# Calcula o número total de amostras
n = len(signal)

# Aplica a FFT e normaliza
fft_values = np.fft.fft(signal)
fft_magnitude = np.abs(fft_values)[:n // 2]  # Considera apenas a metade inferior (frequências positivas)

# Gera o vetor de frequências associado à FFT
frequencies = np.fft.fftfreq(n, d=1 / sampling_rate)[:n // 2]

# Encontra o índice da frequência de maior amplitude (exceto a DC, ou seja, índice > 0)
peak_index = np.argmax(fft_magnitude[1:]) + 1
peak_frequency = frequencies[peak_index]

# Define o limite de 10% do valor máximo
threshold = 0.1 * fft_magnitude.max()

# Encontra o índice da última frequência acima do limite de 10%
max_relevant_index = np.where(fft_magnitude > threshold)[0][-1]
max_relevant_frequency = frequencies[max_relevant_index]

print(f"Frequência dominante: {peak_frequency:.2f} Hz")
print(f"Frequência máxima relevante (10% do pico): {max_relevant_frequency:.2f} Hz")

plt.figure(figsize=(10, 5))
plt.plot(frequencies, fft_magnitude)
plt.axvline(x=peak_frequency, color='r', linestyle='--', label=f'Frequência dominante: {peak_frequency:.2f} Hz')
plt.axvline(x=max_relevant_frequency, color='g', linestyle='--', label=f'Máx. relevante: {max_relevant_frequency:.2f} Hz')
plt.title('Espectro de Frequência (FFT do eixo X)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
