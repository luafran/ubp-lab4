package ubp.lab4.imgproc.worker.entity;

/**
 * Created by lafranll on 9/8/16.
 */
public class TaskEntity {
    public String jobId;
    public String filterId;
    public String originalImageUrl;

    public TaskEntity(String jobId, String filterId, String originalImageUrl) {
        this.jobId = jobId;
        this.filterId = filterId;
        this.originalImageUrl = originalImageUrl;
    }
}
