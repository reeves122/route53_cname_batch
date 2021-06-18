import argparse
import csv
from typing import List

import boto3

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--file_name', '-f', required=True)
PARSER.add_argument('--hosted_zone', '-z', required=True)
PARSER.add_argument('--ttl', '-t', default=300, type=int)
ARGS = PARSER.parse_args()
ROUTE53 = boto3.client('route53')


def build_record_request(name: str, dns_target: str):
    """
    Build a Route53 request structure for a single CNAME record

    :param name:        CNAME record value
    :param dns_target:  Destination DNS target for the CNAME record
    :return:            Route53 record request
    """
    return {
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': name,
            'Type': 'CNAME',
            'TTL': ARGS.ttl,
            'ResourceRecords': [
                {
                    'Value': dns_target
                },
            ],
        }
    }


def create_cname_records(hosted_zone: str, record_changes: List):
    """
    Call AWS to create the set of records requested

    :param hosted_zone:         ID of the AWS Route53 zone
    :param record_changes:      List of Route53 record request items
    :return:                    None
    """
    response = ROUTE53.change_resource_record_sets(
        HostedZoneId=hosted_zone,
        ChangeBatch={
            'Changes': record_changes
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception(f'Route 53 call failed: {response}')


if __name__ == '__main__':
    with open(ARGS.file_name) as f:
        reader = csv.reader(f)
        records = [
            build_record_request(name=row[0].strip(), dns_target=row[1].strip())
            for row in reader
        ]
        print(f'Creating {len(records)} Route 53 records')
        create_cname_records(hosted_zone=ARGS.hosted_zone,
                             record_changes=records)
        print('Done')
