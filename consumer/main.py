import json
import time
import boto3

from cognito_secrets import SecretKeys


secret_keys = SecretKeys()


sqs_client = boto3.client(
    "sqs",
    region_name=secret_keys.REGION_NAME,
)


ecs_client= boto3.client("ecs",region_name=secret_keys.REGION_NAME)

def poll_sqs():

    print(f"------------------------------Region: {secret_keys.REGION_NAME}")
    try:
        while True:
            response = sqs_client.receive_message(
                QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            )
            for message in response.get("Messages", []):
                message_body = json.loads(message.get("body"))
                if (
                    "Service" in message_body
                    and "Event" in message_body
                    and message_body.get("Event") == "s3:TestEvent"
                ):
                    sqs_client.delete_message(
                        QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                    continue

                if "Records" in message_body:
                    s3_records=message_body["Records"][0]["s3"]
                    bucket_name=s3_records["bucket"]["name"]
                    s3_key=s3_records["object"]["key"]

                    # spin up a docker container
                    ecs_client.run_task(
                        cluster="arn:aws:ecs:eu-west-2:414483037181:cluster/your-cluster-name",
                        launchType="FARGATE",
                        taskDefinition="arn:aws:ecs:eu-west-2:414483037181:task-definition/Video-Transcoder:1",
                        overrides={
                            "containerOverrides": [
                                {
                                    "name": "video-transcoder",
                                    "environment": [
                                        {"name": "S3_BUCKET", "value": bucket_name},
                                        {"name": "S3_KEY", "value": s3_key}
                                    ]
                                }
                            ]
                        },
                        networkConfiguration={
                            "awsvpcConfiguration": {
                                "subnets": ["your-subnet-id"],
                                "assignPublicIp": "ENABLED"
                            }
                        }
                    )
                    

            print(response)
            time.sleep(1)
    except Exception as e:
        print(e)


poll_sqs()
