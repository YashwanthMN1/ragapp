import boto3

AWSREGION = "us-east-1"

ssmclient = boto3.client("ssm", region_name=AWSREGION)


def get_current_doc_id():
    response = ssmclient.get_parameter(Name="CURRENT_DOCUMENT_ID", WithDecryption=True)
    return response["Parameter"]["Value"]


def chunk_text(text, counter, chunk_size=200):
    words = text.split()
    chunks = dict()
    num = int(len(words) / chunk_size) + 1
    for i in range(num):
        counter += 1
        chunks[counter] = " ".join(words[i : i + chunk_size])
    return counter, chunks

def store_current_doc_id(doc_id):
    allids = ssmclient.get_parameter(Name="ALL_DOC_IDS", WithDecryption=True)
    document_ids = allids["Parameter"]["Value"].split(",")
    document_ids.append(doc_id)

    allresponse = ssmclient.put_parameter(
        Name="ALL_DOC_IDS",
        Value=",".join(document_ids),
        Type="StringList",
        Overwrite=True,
    )
    response = ssmclient.put_parameter(
        Name="CURRENT_DOCUMENT_ID",
        Value=doc_id,
        Type="SecureString",
        Overwrite=True,
    )
    # return response


