import boto3
import logging

from botocore.exceptions import ClientError

s3 = boto3.client('s3')
delete_marker = 'auto-delete'

# Create and configure logger
logging.basicConfig(filename="cloudcommander-s3-cleanup.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def scan_for_marked_buckets():
    """
    Scan the account/region for Buckets that are tagged for cleanup.

    :rtype: List of Buckets
    """
    # Fetch list of all Buckets
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
    logger.info('Fetching list of all Buckets')
    all_buckets = s3.list_buckets()['Buckets']
    # logger.debug('All buckets found: ' + all_buckets)

    for bucket_dict in all_buckets:
        bucket_name = str(bucket_dict['Name'])
        logger.debug('Found bucket: ' + bucket_name)
        logger.debug('Fetching tags for  bucket: ' + bucket_name + '.')

        try:
            tags = s3.get_bucket_tagging(Bucket=bucket_name)
            logger.debug('Tags for bucket: ' + bucket_name + ' ==> ' + str(tags))

            # Check for delete marker.
            if delete_marker in tags:
                logger.debug("Bucket " + bucket_name + ' contains delete marker.')
            else:
                logger.debug("Bucket " + bucket_name + ' does NOT contain delete marker.')
        # TODO parse the 'tags' dict to extract the strings of each tag so that we can find the delete marker.
        breadcrumb !!!!!!!!!!!!!

        except ClientError:
            logger.debug('Could not find any tags for Bucket ' + bucket_name)


def empty_bucket(bucket_name):
    # suggested by Jordon Philips
    bucket = s3.Bucket(bucket_name)
    bucket.objects.delete()


# ##################################################################################################


scan_for_marked_buckets()

# Credit
# https://stackoverflow.com/users/6017840/mootmoot
# https://stackoverflow.com/a/43328646
