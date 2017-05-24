package ubp.lab4.httpclient;

public interface HTTPClientFactory {
	HTTPClient getClient(String url);
}
