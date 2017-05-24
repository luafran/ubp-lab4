package ubp.lab4.imgproc.worker;

import com.rabbitmq.client.*;
	import org.apache.log4j.ConsoleAppender;
	import org.apache.log4j.Level;
	import org.apache.log4j.Logger;
	import org.apache.log4j.PatternLayout;
	import ubp.lab4.httpclient.HTTPClientFactory;
	import ubp.lab4.httpclient.HttpUrlHTTPClientFactory;

	import java.io.IOException;


	public class Main {
	    private static final String TASK_QUEUE_NAME = "task_queue";

	    public static void main(String[] argv) throws Exception {

		ConsoleAppender console = new ConsoleAppender();
		String PATTERN = "%d [%p|%c|%C{1}] %m%n";
		console.setLayout(new PatternLayout(PATTERN));
		console.setThreshold(Level.DEBUG);
		console.activateOptions();
		Logger.getRootLogger().addAppender(console);

		String rabbitHost = (argv.length > 0 ? argv[0].trim() : "rabbitmq");
		int rabbitPort = (argv.length > 1 ? Integer.parseInt(argv[1].trim()) : 5672);
		System.out.println("rabbitHost: " + rabbitHost + ", rabbitPort: " + rabbitPort);

		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost(rabbitHost);
		factory.setPort(rabbitPort);

		final Connection connection = factory.newConnection();
		final Channel channel = connection.createChannel();

		channel.queueDeclare(TASK_QUEUE_NAME, true, false, false, null);
		System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

		channel.basicQos(1);

		final HTTPClientFactory httpFactory = new HttpUrlHTTPClientFactory();

		final Consumer consumer = new DefaultConsumer(channel) {
		    @Override
		    public void handleDelivery(String consumerTag, Envelope envelope,
					       AMQP.BasicProperties properties, byte[] body) throws IOException {
			String message = new String(body, "UTF-8");

			System.out.println("Received '" + message + "'");
			try {
			    final Worker worker = new Worker(httpFactory);
                    worker.doWork(message);
                } finally {
                    System.out.println(" [x] Done");
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            }
        };
        channel.basicConsume(TASK_QUEUE_NAME, false, consumer);
    }
}
