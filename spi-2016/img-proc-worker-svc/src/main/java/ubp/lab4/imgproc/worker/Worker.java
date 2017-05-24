package ubp.lab4.imgproc.worker;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import com.google.gson.Gson;

import ubp.lab4.httpclient.HTTPClient;
import ubp.lab4.httpclient.HTTPClientFactory;
import ubp.lab4.httpclient.HTTPResponse;
import ubp.lab4.imgproc.worker.entity.FileEntity;
import ubp.lab4.imgproc.worker.entity.JobEntity;
import ubp.lab4.imgproc.worker.entity.StorageInfoEntity;
import ubp.lab4.imgproc.worker.entity.TaskEntity;

import java.io.File;

public class Worker {

    private static final String WORK_DIR = "/tmp";
    private static final String JOBS_SVC_BASE_URL = "http://img-proc-api-svc:8082/jobs/";
    private static final String STORAGE_SVC_BASE_URL = "http://storage-svc:8083/file/";

    static Logger logger = Logger.getLogger(Worker.class);

    private HTTPClientFactory factory = null;

    Worker(HTTPClientFactory factory) {
        this.factory = factory;
    }

    public void doWork(String task) {

        try {

            // Parse Task as json
            Gson gson = new Gson();
            TaskEntity taskEntity = gson.fromJson(task, TaskEntity.class);
            String jobId = taskEntity.jobId;
            String fileUrl = taskEntity.originalImageUrl;
            String fileName = fileUrl.substring(fileUrl.lastIndexOf("/") + 1, fileUrl.length());
            String originalFilePath = WORK_DIR + "/" + fileName;
            String resultFilePath = WORK_DIR + "/" + fileName + "_processed";

            logger.info("New Task -> jobId: " + jobId);
            logger.info("New Task -> filterId: " + taskEntity.filterId);
            logger.info("New Task -> url: " + fileUrl);

            // Get image file from storage-svc
            HTTPClient httpClient = factory.getClient(taskEntity.originalImageUrl);

            HTTPResponse response = httpClient.downloadFile(WORK_DIR);
            int responseCode = response.code;
            String responseData = response.data;
            logger.info("Download response code: " + responseCode);
            logger.info("Download response data: " + responseData);

            if (responseCode >= 200 && responseCode <= 299) {
                logger.info("got file: " + originalFilePath);
            }

            // Process the file
            //GreyScaleFilter filter = new GreyScaleFilter();
            //filter.process(originalFilePath, resultFilePath);

            // Upload processed file to storage-svc
            String fileAsBase64 = Base64.encodeBase64String(FileUtils.readFileToByteArray(new File(originalFilePath)));
            FileEntity file = new FileEntity("image/jpeg", fileAsBase64);
            httpClient = factory.getClient(STORAGE_SVC_BASE_URL);
            httpClient.setHeader("Content-Type", "application/json");
            httpClient.setHeader("Accept", "application/json");
            String body = gson.toJson(file);
            response = httpClient.post(body);
            responseCode = response.code;
            responseData = response.data;
            logger.info("Store file response code: " + responseCode);
            logger.info("Store file response data: " + responseData);
            StorageInfoEntity storageInfo = null;
            if (responseCode >= 200 && responseCode <= 299) {
                Gson gsonResp = new Gson();
                storageInfo = gsonResp.fromJson(responseData, StorageInfoEntity.class);
            }

            String resultUrl = STORAGE_SVC_BASE_URL + storageInfo.fileId;

            // Update job with new status and resultImageUrl
            httpClient = factory.getClient(JOBS_SVC_BASE_URL + jobId);
            httpClient.setHeader("Content-Type", "application/json");
            httpClient.setHeader("Accept", "application/json");
            JobEntity job = new JobEntity(resultUrl, "PROCESSED");
            body = gson.toJson(job);
            response = httpClient.put(body);
            responseCode = response.code;
            responseData = response.data;
            logger.info("Update job response code: " + responseCode);
            logger.info("Update job response data: " + responseData);

        } catch(Exception e) {
            logger.error(e);
        }
    }
}
