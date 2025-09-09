from ftplib import FTP

# FTP server details (replace with real server)
FTP_HOST = "ftp.dlptest.com"   # Free test FTP server
FTP_USER = "dlpuser"           # Public test user
FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu"  # Public test password

# Local files for upload/download
UPLOAD_FILE = r"C:\Users\hp\Downloads\ideaD3.txt"
DOWNLOAD_FILE = "downloaded_ideaD3.txt"

try:
    # 1. Connect to FTP server
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print(" Connected to FTP server")

    # 2. Upload a file
    with open(UPLOAD_FILE, "rb") as f:
        ftp.storbinary(f"STOR {UPLOAD_FILE}", f)
    print(f"Uploaded: {UPLOAD_FILE}")

    # Confirm upload by listing files
    print(" Directory listing after upload:")
    ftp.retrlines("LIST")

    # 3. Download the same file
    with open(DOWNLOAD_FILE, "wb") as f:
        ftp.retrbinary(f"RETR {UPLOAD_FILE}", f.write)
    print(f" Downloaded: {DOWNLOAD_FILE}")

    # 4. Verify downloaded content
    with open(DOWNLOAD_FILE, "r") as f:
        content = f.read()
    print(" Downloaded file content:")
    print(content)

    # Close connection
    ftp.quit()

except Exception as e:
    print(" Error:", e)
