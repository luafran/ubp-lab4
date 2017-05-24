package ubp.lab4.httpclient;

public class HttpUrlHTTPClientFactory implements HTTPClientFactory {

	public HTTPClient getClient(String url) {
		
		return new HttpUrlHTTPClient(url);
	}	
}
