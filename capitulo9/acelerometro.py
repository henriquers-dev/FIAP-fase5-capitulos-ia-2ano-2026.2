import serial
import csv
from datetime import datetime

porta = 'COM3'
baudrate = 115200
arquivo = 'dados_sensor.csv'

try:
    ser = serial.Serial(porta, baudrate, timeout=1)
    print(f"[OK] Conectado à {porta}")

    with open(arquivo, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ax', 'ay', 'az'])

        while True:

            linha=ser.readline().decode(errors='ignore').strip()
            if '-->' in linha:
                try:
                    dados = linha.split('-->')[1].split(',')
                    if len(dados) == 3:
                        ts = datetime.now().isoformat()
                        acc = [float(v) for v in dados]
                        writer.writerow([ts] + acc)
                        print(f"{ts} | AX={acc[0]:.3f}g  AY={acc[1]:.3f}g  AZ={acc[2]:.3f}g")
                except:
                    continue
except Exception as e:
    print(f"[ERRO] Porta {porta} indisponível: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"[FIM] Porta {porta} fechada.")
