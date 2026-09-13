#include <Wire.h>        // Comunicação I2C
#include <MPU6050.h>     // Biblioteca do sensor MPU6050

#define NUM_AMOSTRAS_CALIBRACAO 100   // Quantidade de amostras para calibração
#define INTERVALO_MS 200              // Tempo entre leituras (em milissegundos)

MPU6050 mpu;             // Objeto do sensor MPU6050

int16_t ax, ay, az;      // Variáveis para dados brutos do acelerômetro
float offsetX = 0, offsetY = 0, offsetZ = 0;

void setup() {
  Wire.begin(21, 22);    // Define os pinos I2C (ESP32 Heltec V2: SDA=21, SCL=22)
  Serial.begin(115200);  // Inicia comunicação serial

  mpu.initialize();      // Inicializa o sensor

  // Verifica conexão
  if (!mpu.testConnection()) {
    Serial.println("Erro ao conectar MPU6050.");
    while (1);  // Fica preso aqui se não conseguir conectar
  }

  // Configura faixa de aceleração e filtro
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_4);  // Faixa de ±4g
  mpu.setDLPFMode(MPU6050_DLPF_BW_20);             // Filtro digital de 20 Hz

  // Calibração com número definido de amostras
  calibrarMPU6050(NUM_AMOSTRAS_CALIBRACAO);
  // Imprime cabeçalho para CSV
  Serial.println("AX_g,AY_g,AZ_g");
}

void loop() {
  // Lê aceleração bruta
  mpu.getAcceleration(&ax, &ay, &az);

  // Converte para 'g' com compensação de offset
  float ax_g = (ax - offsetX) / 8192.0;
  float ay_g = (ay - offsetY) / 8192.0;
  float az_g = (az - offsetZ) / 8192.0;

  // Envia via Serial com 3 casas decimais e prefixo "-->"
  Serial.print("-->");
  Serial.print(String(ax_g, 3)); Serial.print(",");
  Serial.print(String(ay_g, 3)); Serial.print(",");
  Serial.println(String(az_g, 3));

  delay(INTERVALO_MS);  // Intervalo entre leituras definido em ms
}

// Função para calibrar o sensor assumindo que está parado
void calibrarMPU6050(int amostras) {
  long somaX = 0, somaY = 0, somaZ = 0;

  for (int i = 0; i < amostras; i++) {
    mpu.getAcceleration(&ax, &ay, &az);
    somaX += ax;
    somaY += ay;
    somaZ += az;
    delay(5);  // Pequeno intervalo entre leituras
  }

  offsetX = somaX / (float)amostras;
  offsetY = somaY / (float)amostras;
  offsetZ = (somaZ / (float)amostras) - 8192.0;  // Compensar gravidade em Z
}
