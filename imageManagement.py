import streamlit as st
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import pandas as pd

# Create a streamlit with a button to upload an image, which should show the image first. Then there should be
# a separate "upload to s3" button to save it in an s3 bucket called "nuj-images" if it exists, else create it and
# upload with a formatting of yyyy-mm-dd-imagefilename

# hint: use boto3 to interact with s3. You can use the following code to create a bucket if it doesn't exist. Use the S3ListBuckets()

# later implement the abilily to create a new folder for every day and upload the images there

st.title("Image Uploader")
bucket_name = "nuj-images"
s3 = boto3.client("s3")

def show_images():
    # List files in bucket and show as table + thumbnails
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in objects:
            data = []
            image_urls = []
            for obj in objects["Contents"]:
                name = obj["Key"]
                date_uploaded = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
                size_kb = round(obj["Size"] / 1024, 2)
                data.append({"Name": name, "Date Uploaded": date_uploaded, "Size (KB)": size_kb})
                # Generate a presigned URL for the image
                if name.lower().endswith((".png", ".jpg", ".jpeg")):
                    url = s3.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": bucket_name, "Key": name},
                        ExpiresIn=3600
                    )
                    image_urls.append((name, url))
            df = pd.DataFrame(data)
            st.table(df)
            if image_urls:
                st.markdown("#### Thumbnails")
                cols = st.columns(4)
                for idx, (name, url) in enumerate(image_urls):
                    with cols[idx % 4]:
                        st.image(url, caption=name, use_container_width=True)
        else:
            st.info("No files found in the bucket.")
    except ClientError as e:
        if hasattr(e, "operation_name") and e.operation_name == "ListObjectsV2":
            pass
        else:
            st.error(f"Could not fetch objects for deletion: {e}")

# Call show_images after a successful upload
show_images()

uploaded_file = st.file_uploader("Select an image", type=["png", "jpg", "jpeg"], key="select")

if uploaded_file is not None:
    img = st.image(uploaded_file, caption="Selected Image", use_container_width=True)

    if st.button("Upload to S3"):
        # Check if bucket exists, else create
        buckets = [b['Name'] for b in s3.list_buckets()['Buckets']]
        if bucket_name not in buckets:
            s3.create_bucket(Bucket=bucket_name)

        # Format filename
        today = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        s3_key = f"{today}-{uploaded_file.name}"
        
        # Upload file
        try:
            s3.upload_fileobj(uploaded_file, bucket_name, s3_key)
            st.success(f"Uploaded to S3 as {s3_key}")
            img.empty()  # Clear the displayed image
            show_images()  # Refresh the image list
            st.rerun()  # Refresh the app to update thumbnails
        except ClientError as e:
            st.error(f"Upload failed: {e}")

def delete_object_from_bucket(object_key):
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        st.success(f"Deleted {object_key} from S3 bucket.")
        st.rerun()
    except ClientError as e:
        st.error(f"Could not delete {object_key}: {e}")

# Dropdown to select and delete an object from the bucket
try:
    objects = s3.list_objects_v2(Bucket=bucket_name)
    object_keys = [obj["Key"] for obj in objects.get("Contents", [])]
    if object_keys:
        selected_object = st.selectbox("Select an object to delete", object_keys, key="delete_select")
        if st.button("Delete"):
            delete_object_from_bucket(selected_object)
    else:
        st.info("No objects available to delete.")
except ClientError as e:
    if hasattr(e, "operation_name") and e.operation_name == "ListObjectsV2":
        pass
    else:
        st.error(f"Could not fetch objects for deletion: {e}")

def delete_bucket():
    try:
        # Check if bucket exists
        buckets = [b['Name'] for b in s3.list_buckets()['Buckets']]
        if bucket_name not in buckets:
            st.error(f"Bucket '{bucket_name}' does not exist.")
            return

        # Check if bucket is empty
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in objects and len(objects["Contents"]) > 0:
            st.error("Bucket is not empty. Please delete all objects before deleting the bucket.")
            return

        s3.delete_bucket(Bucket=bucket_name)
        st.success(f"Bucket '{bucket_name}' deleted successfully.")
        st.rerun()
    except ClientError as e:
        st.error(f"Could not delete bucket: {e}")

# Button to delete the bucket
if st.button("Delete Entire Bucket"):
    delete_bucket()