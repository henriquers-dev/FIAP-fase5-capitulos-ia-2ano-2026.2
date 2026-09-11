#include <WiFi.h> // Biblioteca para conexão Wi-Fi
#include <PubSubClient.h> // Biblioteca para cliente MQTT
#include <WiFiClientSecure.h> // Biblioteca para conexão TLS segura

// Rede Wi-Fi
const char* ssid = "FIAP-IOT"; // Nome da rede Wi-Fi
const char* password = "F!@p25.IOT"; // Senha da rede Wi-Fi

// Broker e credenciais HiveMQ Cloud
const char* mqtt_server = "xxxxxxxxxxxxxxxx.s2.eu.hivemq.cloud"; // Endereço do broker HiveMQ Cloud
const int mqtt_port = 8883; // Porta padrão para conexão TLS (MQTTS)
const char* mqtt_user = "usuarioMQTT"; // Nome de usuário para autenticação no broker
const char* mqtt_password = "senhaMQTT"; // Senha para autenticação no broker

// Certificado ISRG Root X1 (Let's Encrypt)
const char* ca_cert = \ // Certificado digital da autoridade certificadora (CA)
"-----BEGIN CERTIFICATE-----\n"\
"MIIFazCCA1OgAwIBAgISA9Aj.... (truncado)\n"\
"-----END CERTIFICATE-----\n";

WiFiClientSecure espClientTLS; // Cliente com suporte a TLS
PubSubClient client(espClientTLS); // Cliente MQTT baseado no cliente seguro

void setup_wifi() {
  delay(10); // Pequeno atraso inicial
  Serial.println("Conectando ao Wi-Fi...");
  WiFi.begin(ssid, password); // Inicia conexão com Wi-Fi
  while (WiFi.status() != WL_CONNECTED) { // Aguarda conexão
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado"); // Confirma conexão Wi-Fi
}

void reconnect() {
  while (!client.connected()) { // Enquanto o cliente MQTT não estiver conectado
    Serial.print("Conectando ao broker MQTT (TLS)... ");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) { // Tenta conectar com usuário e senha
      Serial.println("Conectado!");
    } else {
      Serial.print("Falha, rc="); // Em caso de falha, mostra o código de erro
      Serial.print(client.state());
      delay(5000); // Aguarda 5 segundos antes de tentar novamente
    }
  }
}

void setup() {
  Serial.begin(115200); // Inicializa comunicação serial
  espClientTLS.setCACert(ca_cert); // Carrega o certificado CA para validar o broker
  setup_wifi(); // Executa a função de conexão Wi-Fi
  client.setServer(mqtt_server, mqtt_port); // Configura o endereço e porta do broker MQTT
}

void loop() {
  if (!client.connected()) { // Se estiver desconectado do broker, tenta reconectar
    reconnect();
  }
  client.loop(); // Mantém a conexão MQTT ativa

  String payload = "{\"sensor\":\"HC-SR04\",\"valor\":42.15,\"unidade\":\"cm\"}"; // Monta a mensagem JSON
  client.publish("sensor/movimento", payload.c_str()); // Publica a mensagem no tópico especificado
  Serial.print("Enviado (TLS): "); // Mostra no monitor serial a mensagem enviada
  Serial.println(payload);
  delay(1000); // Aguarda 1 segundo antes de enviar novamente
}
