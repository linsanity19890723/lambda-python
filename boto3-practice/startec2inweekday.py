import boto3
import os
import datetime

print('Loading function')


def lambda_handler(event, context):
    instance_start()


def instance_start():
    ec2 = boto3.client('ec2', region_name='ap-southeast-1')
    desc = ec2.describe_instances(Filters=[{'Name': 'tag:project', "Values": ['Auto']}])

    targets = []
    for reservation in desc['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:

                    # タグが isSchedule の場合に、値が true を対象
                    if tag['Key'] == 'project' and tag['Value'] == 'Auto':
                        targets.append(instance['InstanceId'])
    print(targets)
    tages = []
    for reservation in desc['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    # タグが isSchedule の場合に、値が true を対象
                    # if tag['Key'] is not null:
                    #         tags.append(instance['Key'])
                    if tag['Key'] == 'project' and tag['Value'] == 'Auto':
                        targets.append(instance['InstanceId'])
                    for i in targets:
                        if tag['Key'] == 'Name':
                            tages.append(tag['Value'])
    tagesremove = list(set(tages))
    print(tagesremove)
    tagesremove = [os.environ['instanceid']]

    status = desc['Reservations'][0]['Instances'][0]['State']['Name']
    print(status)

    # tag = desc['Reservations'][0]['Instances'][0]['Tags']
    # print(tag)
    day = datetime.date.today()
    today = day.strftime("%Y%m%d")
    week = day.weekday()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('holidays-tw')
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
        # elif  week == 6:
        message = "today is weekend"
        print('today is weekend')
    elif check == False:
        print("bad day")
        if status == "running":
            message = "instance is already running. nothing to do"
        elif status == "stopped":
            # ec2.start_instances(InstanceIds=[os.environ['instanceid']])
            ec2.start_instances(InstanceIds=targets)
            message = "instance start"
        else:
            message = "instance is not stopped. can not start instance"
    else:
        message = "holiday check is failed"
    sns_publish(message)


def sns_publish(message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn='arn:aws:sns:ap-southeast-1:405222713477:AutoStopStartNotification',
        Message=message,
        Subject='[' + os.environ['instanceid'] + ']:startup_instance'
    )






