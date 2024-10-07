import mysql.connector
from sys import argv
import os
from minio import Minio
from minio.error import S3Error

hostname = argv[1] if len(argv) > 1 else "127.0.0.1"
port = int(argv[2]) if len(argv) > 2 else 3307
user = argv[3] if len(argv) > 3 else "ninetofiver"
password = argv[4] if len(argv) > 4 else "ninetofiver"
media_path = argv[5] if len(argv) > 5 else "./media"
dbname = argv[6] if len(argv) > 6 else "ninetofiver"
miniourl = argv[7] if len(argv) > 7 else "127.0.0.1:9000"
minio_access = argv[8] if len(argv) > 8 else "minio"
minio_secret = argv[9] if len(argv) > 9 else "minio-client"
bucket = argv[10] if len(argv) > 10 else "media"

if not os.path.exists(os.path.abspath(media_path)):
    print(f"File path '{os.path.abspath(media_path)}' does not exist.")
    exit(1)

try:
    db = mysql.connector.connect(
        host=hostname,
        user=user,
        password=password,
        database=dbname,
        port=port
    )
except mysql.connector.Error as error:
    print("Could not connect to MySQL database")
    print(error)
    exit(1)

client = Minio(miniourl, access_key=minio_access, secret_key=minio_secret, secure=False)

if not client.bucket_exists(bucket_name=bucket):
    print(f"Bucket '{bucket}' does not exist, creating")
    client.make_bucket(bucket)

cursor = db.cursor(dictionary=True)
cursor.execute("SELECT * from ninetofiver_attachment")
rows = cursor.fetchall()

def update_mysql_record(db, file_id, new_url):
    try:
        cursor.execute(f"UPDATE ninetofiver_attachment SET file='{new_url}' WHERE id={file_id}")
        db.commit()
        print(f"Successfully updated record for file ID {file_id}")
    except mysql.connector.Error as error:
        print(f"Could not update record for file ID {file_id}")
        print(error)

for row in rows:
    path = row["file"]
    # Check if the file exists in the media folder
    if not os.path.exists(os.path.join(os.path.abspath(media_path), path)):
        continue  # File does not exist, skipping
    client.fput_object(bucket, path, os.path.join(os.path.abspath(media_path), path))
    print(f"Successfully added {os.path.join(os.path.abspath(media_path), path)} to bucket {bucket}")
