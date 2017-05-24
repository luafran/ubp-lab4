package ubp.lab4.imgproc.worker.entity;

public class FileEntity {
    public String contentType;
    public String content;

    public FileEntity(String contentType, String content) {
        this.contentType = contentType;
        this.content = content;
    }
}
