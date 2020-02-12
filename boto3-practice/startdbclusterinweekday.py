import boto3
import os
import datetime

DB_CLUSTER_IDENTIFIER = os.environ['DB_CLUSTER_IDENTIFIER']


def lambda_handler(event, context):
    dbcluster_start()


def dbcluster_start():
    db_client = boto3.client('rds', region_name='ap-northeast-1')
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
    bucket = s3.Bucket('tw-holiday-data')
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
        if status == "running":
            message = "dbcluster is already running. nothing to do"
        elif status == "stopped":
            db_client.start_db_cluster(DBClusterIdentifier=DB_CLUSTER_IDENTIFIER)
            message = "dbcluster start"
        else:
            message = "dbcluster is not stopped. can not start instance"
    else:
        message = "holiday check is failed"
    sns_publish(message)


def sns_publish(message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn='arn:aws:sns:ap-northeast-1:849700601919:sendmail',
        Message=message,
        Subject='[' + os.environ['DB_CLUSTER_IDENTIFIER'] + ']:startup_dbcluster'

    )