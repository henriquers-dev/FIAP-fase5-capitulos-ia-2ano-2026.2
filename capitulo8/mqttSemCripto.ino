const char* ssid = "FIAP-IOT";
const char* password = "F!@p25.IOT";

const char* broker = "192.168.137.1";
const int port = 1883;
const char* topico = "sensor/distancia";

WiFiClient espClient;
PubSubClient client(espClient);

#define TRIGGER 33
#define ECHO 32

// Protótipos (necessários em .cpp puro)
void conectarWiFi();
void reconectarMQTT();
float medirDistancia();
void enviarMQTT(float valor);

void setup() {
  Serial.begin(115200);
  pinMode(TRIGGER, OUTPUT);
  pinMode(ECHO, INPUT);
  conectarWiFi();
  client.setServer(broker, port);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi caiu, reconectando...");
    conectarWiFi();
  }

  if (!client.connected()) {
    reconectarMQTT();
  }

  client.loop();

  float distancia = medirDistancia();

  if (distancia >= 0) {
    enviarMQTT(distancia);
  } else {
    Serial.println("Leitura inválida, não publicado.");
  }

  delay(3000);
}

void conectarWiFi() {
  Serial.print("Conectando-se ao Wi-Fi");
  WiFi.begin(ssid, password);

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 40) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi conectado");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao conectar ao Wi-Fi. Tentando novamente no próximo ciclo.");
  }
}

void reconectarMQTT() {
  int tentativas = 0;
  while (!client.connected() && tentativas < 5) {
    Serial.print("Conectando ao broker MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado");
    } else {
      Serial.print("Falha, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
      tentativas++;
    }
  }
}

float medirDistancia() {
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER, LOW);

  long duracao = pulseIn(ECHO, HIGH, 30000);

  if (duracao == 0) {
    Serial.println("Sem eco recebido (fora de alcance ou erro no sensor)");
    return -1;
  }

  float distancia = duracao * 0.034 / 2;
  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.println(" cm");
  return distancia;
}

void enviarMQTT(float valor) {
  char mensagem[20];
  dtostrf(valor, 4, 2, mensagem);

  if (client.publish(topico, mensagem)) {
    Serial.print("Publicado: ");
    Serial.println(mensagem);
  } else {
    Serial.println("Falha ao publicar MQTT");
  }
}

#else

void setup() {
  Serial.begin(115200);
  Serial.println("Bibliotecas WiFi e PubSubClient nao foram encontradas.");
  Serial.println("Instale o suporte ESP32 e a biblioteca PubSubClient para compilar este projeto.");
}

void loop() {
  delay(1000);
}

#endif
