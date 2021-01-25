from google.cloud import storage
import glob
import argparse
import os

tmp = os.getcwd()
abs_dirname = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(abs_dirname, "env/general-storage-299702-e4dc4bbd7d8c.json")

BUCKET_NAME = "fudepolygon_2020"
STORAGE_CLASS = "COLDLINE"
LOCATION = "us-east1"
SOURCE_DIR = "fudepolygon_data/"

def create_bucket(storage_cl, storage_class: str=STORAGE_CLASS, location: str=LOCATION, bucket_name: str=BUCKET_NAME):
	bucket = storage_cl.bucket(bucket_name)
	bucket.storage_class = storage_class
	new_bucket = storage_cl.create_bucket(bucket, location=location)
	print("\n")
	print(
		"Created bucket {} in {} with storage class {}\n".format
			(new_bucket.name, new_bucket.location, new_bucket.storage_class)
	)
	return new_bucket

def upload_data_to_bucket(storage_cl, bucket_name: str, source_dir: str=SOURCE_DIR):
	bucket = storage_cl.bucket(bucket_name)
	for path in sorted(glob.glob(source_dir + "*")):
		blob = bucket.blob(path)
		blob.upload_from_filename(path)
		print("File {} uploaded to {}.".format(path, bucket.name))
	print("Finish uploading!")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='gcsにデータをuplodするスクリプト')
	parser.add_argument('--source_dir', type=str, help='データがあるpath')
	args = parser.parse_args()
	# gcsにアップロード
	strage_cl = storage.Client()
	bucket = create_bucket(strage_cl, STORAGE_CLASS, LOCATION)
	upload_data_to_bucket(strage_cl, bucket.name, args.source_dir)
