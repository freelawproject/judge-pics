import argparse
import glob
import json
import os
from pathlib import Path

import boto3
from boto3.s3.transfer import S3Transfer
from PIL import Image
from resizeimage import resizeimage

sizes = ["128", "256", "512", "orig"]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR.split("/")[-1] != "judge_pics":
    raise RuntimeError("Please run update from the judge_pics directory")


def upload(
    file_path: str, aws_path: str, access_key: str, secret_key: str
) -> None:
    """Uploads a file to an S3 bucket.

    :param file_path: File to upload
    :param aws_path: The path in the S3 bucket
    :param access_key: The access key for the S3
    :param secret_key: The secret key for the S3
    :return: None
    """
    # bucket = "dev-com-courtlistener-storage"
    bucket = "portraits.free.law"
    client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    transfer = S3Transfer(client)
    transfer.upload_file(
        file_path,
        bucket,
        aws_path,
        extra_args={"ContentType": "image/jpeg", "ACL": "public-read"},
    )
    print(f"http://{bucket}.s3-us-west-2.amazonaws.com/{aws_path}")


def resize_image(original: str, size: str) -> str:
    """Resize an image.

    :param original: The path to the original image
    :param size: The size of the image width to resize
    :return: The path to the new resized image
    """
    new_filepath = original.replace("orig", size)
    if not os.path.exists(os.path.dirname(new_filepath)):
        os.mkdir(os.path.dirname(new_filepath))
    with open(original, "rb") as f:
        img = Image.open(f)
        img = resizeimage.resize_height(img, int(size), validate=False)
        img.save(new_filepath, img.format)
    return new_filepath


def validate_json() -> bool:
    """Validate the json file contains our new judges

    :return: True if valid, else Raises an exception
    """
    with Path(ROOT_DIR, "data", "people.json").open(encoding="utf-8") as f:
        judges = json.load(f)

    judges_in_json = [f'{v["path"]}.jpeg' for v in judges]

    portraits = [
        x.split("/")[-1] for x in glob.glob(f"{ROOT_DIR}/data/orig/*.jpeg")
    ]

    missing_judges = sorted(list(set(judges_in_json) ^ set(portraits)))
    if not missing_judges:
        return True

    raise ValueError(f"Missing entry for: {' '.join(missing_judges)}")


def find_new_portraits(access_key: str, secret_key: str) -> list:
    """Compare s3 and local to find new portraits.

    :param access_key: Access key
    :param secret_key: Secret key
    :return: List of new portraits to process
    """
    session = boto3.Session(
        aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket("portraits.free.law")
    aws_portraits = [
        x.key.split("/")[-1] for x in bucket.objects.filter(Prefix="v2/orig/")
    ]
    local_portraits = [
        x.split("/")[-1] for x in glob.glob(f"{ROOT_DIR}/data/orig/*.jpeg")
    ]
    judges_to_upload = set(aws_portraits) ^ set(local_portraits)
    return sorted(list(judges_to_upload))


def main(access_key: str, secret_key: str) -> None:
    """Resize and upload new portraits to S3.

    :param access_key: The s3 access key
    :param secret_key: The s3 secret key
    :return: None
    """
    # Check for duplicate judge files
    validate_json()

    # Check for files we need to upload
    judges_to_upload = find_new_portraits(access_key, secret_key)

    # Generate new file sizes and upload them to the server
    for judge in list(judges_to_upload):
        for size in sizes:
            filepath = f"{ROOT_DIR}/data/orig/{judge}"
            aws_path = f"v2/{size}/{judge}"
            if size != "orig":
                filepath = resize_image(filepath, size)
                aws_path.replace("orig", size)
            upload(filepath, aws_path, access_key, secret_key)


if __name__ == "__main__":
    # This is mostly meant to be called from the github action but it could be
    # called locally with the correct credentials.
    parse = argparse.ArgumentParser(description="Create a new portrait")
    parse.add_argument(
        "--access-key", "-a", help="The access key", required=True
    )
    parse.add_argument(
        "--secret-key", "-s", help="The secret key", required=True
    )
    args = parse.parse_args()
    main(access_key=args.access_key, secret_key=args.secret_key)
