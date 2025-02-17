import boto3

ssmclient = boto3.client("ssm", region_name="us-east-1")


def get_current_doc_id():
    """
    gets the current document id from the parameter store.

    returns:
        str: The current document id.
    """
    response = ssmclient.get_parameter(Name="CURRENT_DOCUMENT_ID", WithDecryption=True)
    return response["Parameter"]["Value"]


def chunk_text(text, counter, chunk_size=200):
    """
    splits a given text into chunks of a given size.

    args:
        text (str): The text to split.
        counter (int): A counter to keep track of the chunks.
        chunk_size (int, optional): The size of each chunk. Defaults to 200.

    returns:
        tuple: A tuple containing the updated counter and a dictionary with the chunks.
    """
    words = text.split()
    chunks = dict()
    num = int(len(words) / chunk_size) + 1
    for i in range(num):
        counter += 1
        chunks[counter] = " ".join(words[i : i + chunk_size])
    return counter, chunks

def store_current_doc_id(doc_id):
    """
    stores the given document id as the current document id in the system's secure parameter store.

    args:
        doc_id (str): The new document id to set as the current document.

    returns:
        dict: A dictionary containing a response message indicating whether 
              the document id was updated successfully or not.
    """
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


