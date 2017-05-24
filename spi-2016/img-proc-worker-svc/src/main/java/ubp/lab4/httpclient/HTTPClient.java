package ubp.lab4.httpclient;

public interface HTTPClient {

	void setHeader(String property, String value);

	HTTPResponse get();

	HTTPResponse post(String body);

	HTTPResponse put(String body);

    HTTPResponse downloadFile(String saveDir);
}