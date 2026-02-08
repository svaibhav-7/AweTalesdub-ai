
import os

filename = "verify_output_v6.txt"
if os.path.exists(filename):
    with open(filename, "rb") as f:
        f.seek(0, 2)  # Seek to end
        filesize = f.tell()
        seek_pos = max(0, filesize - 1000)
        f.seek(seek_pos)
        last_bytes = f.read()
        print(f"Last 1000 bytes of {filename}:")
        decoded = last_bytes.decode('utf-8', errors='replace')
        print(f"Decoded (ascii): {ascii(decoded)}")
else:
    print(f"{filename} not found.")
