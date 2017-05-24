package ubp.lab4.httpclient;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
//import org.apache.log4j.Logger;


public class HttpUrlHTTPClient implements HTTPClient {
	
	//static Logger logger = Logger.getLogger(HTTPConnection.class);

    private static final int BUFFER_SIZE = 4096;

    private String url = null;
	private HttpURLConnection httpConnection = null;
	
	public HttpUrlHTTPClient(String url) {
		try {
            this.url = url;
			URL urlObj = new URL(url);
			
			this.httpConnection = (HttpURLConnection) urlObj.openConnection();
			httpConnection.setConnectTimeout(5000);
			httpConnection.setReadTimeout(5000);
			httpConnection.setDoOutput(true); 
			httpConnection.setDoInput(true);
		}
		catch(Exception e) {
			//logger.error(e);
		}
	}
	
	public void setHeader(String property, String value) {
		httpConnection.setRequestProperty(property, value);
	}
	
	public HTTPResponse get() {
		
		//logger.debug("GET " + httpConnection.getURL().toString());
		
		HTTPResponse response = new HTTPResponse(999, "Internal Error");
		
		try {
			httpConnection.setRequestMethod("GET");
			response = buildResponse();
		}  catch (Exception e) {
			//logger.error(e);
		}	
		
		return response;
	}
	
	public HTTPResponse post(String body) {
		
		//logger.debug("POST " + httpConnection.getURL().toString());
		//logger.debug("body: " + body);
		
		HTTPResponse response = new HTTPResponse(999, "Internal Error");
		
		try {
			httpConnection.setRequestMethod("POST");
			writeBody(body);
			response = buildResponse();
			
		} catch (Exception e) {
			//logger.error(e);
		}
		
		return response;
	}
	
	public HTTPResponse put(String body) {
		
		//logger.debug("PUT " + httpConnection.getURL().toString());
		//logger.debug("body: " + body);
		
		HTTPResponse response = new HTTPResponse(999, "Internal Error");
		
		try {
			httpConnection.setRequestMethod("PUT");
			writeBody(body);
			response = buildResponse();
			
		} catch (Exception e) {
			//logger.error(e);
		}
		
		return response;
	}

    public HTTPResponse downloadFile(String saveDir) {

        int responseCode = 999;
        String responseStr = "Internal Error";
        HTTPResponse response;

        try {
            httpConnection.setRequestMethod("GET");

            responseCode = httpConnection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                String fileName = "";
                String disposition = httpConnection.getHeaderField("Content-Disposition");
                String contentType = httpConnection.getContentType();
                int contentLength = httpConnection.getContentLength();

                if (disposition != null) {
                    // extracts file name from header field
                    int index = disposition.indexOf("filename=");
                    if (index > 0) {
                        fileName = disposition.substring(index + 10,
                                disposition.length() - 1);
                    }
                } else {
                    // extracts file name from URL
                    fileName = url.substring(url.lastIndexOf("/") + 1, url.length());
                }

                System.out.println("Content-Type = " + contentType);
                System.out.println("Content-Disposition = " + disposition);
                System.out.println("Content-Length = " + contentLength);
                System.out.println("fileName = " + fileName);

                // opens input stream from the HTTP connection
                InputStream inputStream = httpConnection.getInputStream();
                String saveFilePath = saveDir + File.separator + fileName;

                // opens an output stream to save into file
                FileOutputStream outputStream = new FileOutputStream(saveFilePath);

                int bytesRead;
                byte[] buffer = new byte[BUFFER_SIZE];
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }

                outputStream.close();
                inputStream.close();

                responseStr = "OK";
                System.out.println("File downloaded");
            } else {
                responseStr = "ERROR";
                System.out.println("No file to download. Server replied HTTP code: " + responseCode);
            }
            httpConnection.disconnect();

        } catch (Exception e) {
            //logger.error(e);
        }

        response = new HTTPResponse(responseCode, responseStr);
        return response;
    }

	
	private void writeBody(String body) {
		DataOutputStream wr;
		try {
			wr = new DataOutputStream(httpConnection.getOutputStream());
			wr.writeBytes(body);
			wr.flush();
			wr.close();
		} catch (IOException e) {
			//logger.error(e);
		}
	}
	
	private HTTPResponse buildResponse() throws IOException {
		
		String inputLine;
		StringBuffer responseData = new StringBuffer();
		BufferedReader in;
		int responseCode = httpConnection.getResponseCode();
		if (responseCode >= 200 && responseCode <= 299) {
			in = new BufferedReader(new InputStreamReader(httpConnection.getInputStream()));	
		}
		else {
			in = new BufferedReader(new InputStreamReader(httpConnection.getErrorStream()));	
		}
		
		while ((inputLine = in.readLine()) != null) {
			responseData.append(inputLine);
		}
		in.close();
		
		HTTPResponse response = new HTTPResponse(responseCode, responseData.toString());
		
		return response;
	}
}
