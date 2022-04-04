import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

/* Kleines Beispiel für die Verwendung von MQTT in Java: Publish */

public class PublishTest {
	static int count = 0;

	public static void main(String[] args) {
		String topic = "notify";
		String content = "";
		int qos = 2;
		String broker = "tcp://localhost:1883";
		String clientId = "Java Client";
		MqttClient client;
		MemoryPersistence persistence = new MemoryPersistence();

		try {
			client = new MqttClient(broker, clientId, persistence);
			MqttCallback callback = new MqttCallback() { //Wird aufgerufen, wenn z.B. eine Nachricht reinkommt

				public void connectionLost(Throwable cause) {
					System.out.println("Connection lost");
				}

				public void messageArrived(String topic, MqttMessage message) throws Exception {
					System.out.println(topic);
					if(topic.equals("pictures")) {
						String m = new String(message.getPayload());
						Path path = Paths.get("picture");
						byte[] strToBytes = Base64.getDecoder().decode(m);
						System.out.println("FOTO:\n"+m);
						Files.write(path, strToBytes);
						System.out.println(path.toString());
						PublishTest.count ++;
						System.out.println(PublishTest.count);
					}
				}

				public void deliveryComplete(IMqttDeliveryToken token) {
					System.out.println("Delivery Complete");
				}
			};
			MqttConnectOptions connOpts = new MqttConnectOptions();
			connOpts.setCleanSession(true);
			connOpts.setUserName("felix");

			client.setCallback(callback);
			System.out.println("Connecting to broker: " + broker);
			client.connect(connOpts);
			client.subscribe("pictures");
			System.out.println("Connected");

			System.out.println("Publishing message: " + content);
			MqttMessage message = new MqttMessage(content.getBytes());
			message.setQos(qos);
			client.publish(topic, message);

		} catch (MqttException me) {
			me.printStackTrace();
		}


	}
}
