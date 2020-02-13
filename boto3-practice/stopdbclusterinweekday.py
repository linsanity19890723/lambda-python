import boto3
import os
import datetime

DB_CLUSTER_IDENTIFIER = os.environ['DB_CLUSTER_IDENTIFIER']


def lambda_handler(event, context):
    dbcluster_stop()


def dbcluster_stop():
    db_client = boto3.client('rds', region_name='ap-southeast-1')
    db_data = db_client.describe_db_clusters(DBClusterIdentifier=DB_CLUSTER_IDENTIFIER)
    print(db_data)
    status = db_data['DBClusters'][0]['Status']
    print(status)
    # for db_cluster in status['DBClusters']:
    #     print(db_cluster['DBClusterIdentifier'])
    day = datetime.date.today()
    today = day.strftime("%Y%m%d")
    week = day.weekday()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('tw-holiday')
    obj = bucket.Object('holiday.txt')
    with open('/tmp/holiday.txt', 'wb') as data:
        obj.download_fileobj(data)
    f = open('/tmp/holiday.txt')
    holidays = f.readlines()
    f.close()
    os.remove('/tmp/holiday.txt')

    check = today + "\n" in holidays
    print(check)

    if check == True:
        message = "today is holiday"
    elif week == 5 or week == 6:
        message = "today is weekend"
    elif check == False:
        print("bad day")
        if status == "stopped":
            message = "dbcluster is already stopped. nothing to do"
        elif status == "available":
            db_client.stop_db_cluster(DBClusterIdentifier=DB_CLUSTER_IDENTIFIER)
            message = "dbcluster stop"
        else:
            message = "dbcluster is not running. can not stop instance"
    else:
        message = "holiday check is failed"
    sns_publish(message)


def sns_publish(message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn='arn:aws:sns:ap-southeast-1:446876986950:stagingdb',
        Message=message,
        Subject='[' + os.environ['DB_CLUSTER_IDENTIFIER'] + ']:stop_dbcluster'

    )