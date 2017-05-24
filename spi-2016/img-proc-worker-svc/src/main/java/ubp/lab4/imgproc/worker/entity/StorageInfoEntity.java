package ubp.lab4.imgproc.worker.entity;

public class StorageInfoEntity {
    public String status;
    public String fileId;

    public StorageInfoEntity(String status, String fileId) {
        this.status = status;
        this.fileId = fileId;
    }
}
