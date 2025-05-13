import boto3
from datetime import datetime, timedelta

def delete_old_files_in_s3(bucket_name, prefix='', days_old=5):
    """
    Finds and deletes S3 objects older than the specified number of days.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str, optional): The prefix to filter objects by. Defaults to ''.
        days_old (int, optional): The number of days to consider a file old. Defaults to 5.

    Returns:
        list: A list of S3 objects that were deleted.
    """

    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    deleted_files = []
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                last_modified = obj['LastModified']
                if last_modified < datetime.now() - timedelta(days=days_old):
                    try:
                        s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                        deleted_files.append(obj['Key'])
                    except Exception as e:
                        print(f"Error deleting {obj['Key']}: {e}")

    return deleted_files

# Example usage:
bucket_name = 'your-bucket-name'
prefix = 'your-prefix'  # Optional: Specify a prefix to filter objects
days_old = 5

deleted_files = delete_old_files_in_s3(bucket_name, prefix, days_old)

if deleted_files:
    print(f"Deleted {len(deleted_files)} old files:")
    for file in deleted_files:
        print(file)
else:
    print("No old files found or no files were deleted.")