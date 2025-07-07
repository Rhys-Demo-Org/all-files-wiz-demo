import com.pulumi.Pulumi;
import com.pulumi.aws.s3.Bucket;
import com.pulumi.aws.s3.BucketArgs;
import com.pulumi.core.Output;

public class App {
    public static void main(String[] args) {
        Pulumi.run(ctx -> {
            // Creates a new S3 bucket.
            var bucket = new Bucket("my-insecure-bucket", BucketArgs.builder()
                // THIS IS THE INSECURE PART.
                // Setting the acl to "public-read" makes all objects in the bucket
                // publicly accessible to anyone on the internet.
                .acl("public-read")
                .build());

            // Exports the name of the bucket.
            ctx.export("bucketName", bucket.id());
        });
    }
}