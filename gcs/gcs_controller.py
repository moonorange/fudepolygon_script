from google.cloud import storage
import glob
from constants import *

BUCKET_NAME = "fudepolygon_2020"

class GcsController:
	def __init__(self, storage_cl):
		self.storage_cl = storage_cl

	def create_bucket(self, storage_class: str, location: str, bucket_name: str = BUCKET_NAME):
		bucket = self.storage_cl.bucket(bucket_name)
		bucket.storage_class = storage_class
		new_bucket = self.storage_cl.create_bucket(bucket, location="us-east1")
		print("\n")
		print(
			"Created bucket {} in {} with storage class {}".format
				(new_bucket.name, new_bucket.location, new_bucket.storage_class)
		)
		return new_bucket

	def upload_data_to_bucket(self, bucket_name: str, source_dir: str = FUDEPOLYGONS_DIR):
		bucket = self.storage_cl.bucket(bucket_name)
		for path in glob.glob(source_dir + "*"):
			import ipdb;ipdb.set_trace()
			blob = bucket.blob(path)
			blob.upload_from_filename(path)
			print("File {} uploaded to {}.".format(path, path))
