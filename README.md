# route53_cname_batch
This is a script to create CNAME batch records to AWS Route53 from a text file.

## Usage

1. Create a CSV text file with all the records you want to create, in this format:
   
    `<cname value>, <destination value>`

2. Run the python script as follows. (Note: Zone ID is not the domain name)

    `python3 route53_cname_batch.py --file_name records.txt --hosted_zone <zone id> --ttl 300` 
