# Image Management using AWS S3

A Streamlit web application for uploading, viewing, and managing images in an AWS S3 bucket. This project provides a simple interface to upload images, view thumbnails, and manage files and buckets directly from your browser.

## Features

- **Image Upload**: Select and preview images before uploading.
- **S3 Integration**: Upload images to an S3 bucket (`nuj-images`). Automatically creates the bucket if it does not exist.
- **Date-based Naming**: Uploaded images are named with the current date and time for easy organization (format: `yyyy-mm-dd-HH_MM_SS-filename`).
- **Image Gallery**: View all images in the bucket as a table and as thumbnails.
- **Delete Images**: Select and delete individual images from the bucket.
- **Delete Bucket**: Option to delete the entire S3 bucket (only if empty).

## Requirements

- Python 3.7+
- AWS credentials with S3 access (configured via environment variables or AWS CLI)

### Python Packages
- `streamlit`
- `boto3`
- `pandas`

Install dependencies using pip:

```bash
C:/Users/<YOUR_USER_NAME>/projects/AWSImageManagement/Image-Management-using-AWS-S3/.venv/Scripts/python.exe -m pip install streamlit boto3 pandas
```

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/TanujGaikwad/Image-Management-using-AWS-S3.git
cd Image-Management-using-AWS-S3
```

2. **Set up AWS credentials**

Ensure your AWS credentials are configured. You can use the AWS CLI or set environment variables:

```bash
aws configure
```

Or set environment variables:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

3. **Create and activate a virtual environment**

A virtual environment is already set up in `.venv`. If not, create one:

```bash
python -m venv .venv
.venv\Scripts\activate
```

4. **Install dependencies**

```bash
.venv\Scripts\pip install -r requirements.txt
```

Or install manually as shown above.

## Usage

Run the Streamlit app:

```bash
.venv\Scripts\streamlit run imageManagement.py
```

The app will open in your browser. You can:
- Upload and preview images
- Upload to S3 with a single click
- View all images and thumbnails
- Delete individual images
- Delete the entire bucket (if empty)

## Notes
- The S3 bucket name is hardcoded as `nuj-images`.
- Images are named with the current date and time for uniqueness.
- Only image files (`.png`, `.jpg`, `.jpeg`) are supported.
- Deleting the bucket is only possible if it is empty.

## License

MIT License

---

*Developed by Tanuj Gaikwad. Contributions welcome!*
