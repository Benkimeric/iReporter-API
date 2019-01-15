from flask_restful import Resource
from flask import jsonify, request
from flask_restful import reqparse
from .validation import Validation
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..models.media_model import *
import boto3
import botocore

from ..models.incidents_model import Incidents

S3_BUCKET = "benkim-ireporter"
S3_KEY = "AKIAIXYVHAZPT6WOZYCA"
S3_SECRET = "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"
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """upload file to amazon s3"""

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Error occured: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)


class UploadImage(Resource, IncidentsMedia):
    """contains method to add image to incidents"""
    @jwt_required
    def patch(self, type, incident_id, media):
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = upload_file_to_s3(file, S3_BUCKET)
            return self.add_image(media, type, incident_id, file_path)
        else:
            return {'Failed to upload file'}
