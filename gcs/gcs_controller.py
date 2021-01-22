from google.cloud import storage
import glob
from constants import *

BUCKET_NAME = "fudepolygon_2020"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "env/general-storage-299702-51e03463833e.json"

class GcsController:
	def __init__(self, storage_cl):
		self.storage_cl = storage_cl

	def create_bucket(self, storage_class, location):
		bucket = self.storage_cl.bucket(BUCKET_NAME)
		bucket.storage_class = storage_class
		self.storage_cl.get_bucket(BUCKET_NAME)
		new_bucket = self.storage_cl.create_bucket(bucket, location=location)
		print(
			"Created bucket {} in {} with storage class {}".format
				(new_bucket.name, new_bucket.location, new_bucket.storage_class)
		)
		return new_bucket

	def upload_data_to_bucket(self, bucket_name, source_dir=FUDEPOLYGONS_DIR):
		bucket = self.storage_cl.bucket(bucket_name)
		for path in glob.glob(source_dir + "*"):
			import ipdb;ipdb.set_trace()
			blob = bucket.blob(path)
			blob.upload_from_filename(path)
			print("File {} uploaded to {}.".format(path, path))
