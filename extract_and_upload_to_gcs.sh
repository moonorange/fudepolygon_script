source .venv/bin/activate
python download_polygons.py --pref all
python gcs/upload_data_to_gcs.py
