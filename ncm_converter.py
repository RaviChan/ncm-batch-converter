# This file is part of https://github.com/RaviChan/ncm-batch-converter,
# which is licensed under the GNU General Public Licence v3.
"""
NCM to MP3/FLAC Converter

This script converts Netease Cloud Music (.ncm) files to standard audio formats
(MP3/FLAC) while preserving metadata and album art.

Usage:
    python3 ncm_converter.py /path/to/input/folder [/path/to/output/folder]

If no output folder is specified, converted files will be saved in the current
working directory.

Features:
- Batch conversion of NCM files
- Preserves original metadata (title, artist, album)
- Retains album artwork
- Automatically installs required dependencies

Copyright (c) 2024 Ravi Chan
Copyright (c) 2025 trustedinster@outlook.com
Licence: GPL-3.0-or-later  # 替换为GPL协议

For more information and updates, visit:
https://github.com/trustedinster/ncm-batch-converter-gui
"""

import logging
import os
import sys
from datetime import datetime

try:
    import binascii
    import struct
    import base64
    import json
    from Crypto.Cipher import AES
    from mutagen import mp3, flac, id3
    from Crypto.Cipher import AES
    from mutagen import flac
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3, APIC
    from mutagen.mp3 import MP3
except ImportError:
    print(
        "Please install the required packages by running this:\npip install -r requirements.txt\n请运行以下命令安装所需的软件包：\npip install -r requirements.txt")
    sys.exit(1)
os.makedirs(".\\log\\", exist_ok=True)
filename = ".\\log\\" + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".log"
logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler(filename, mode="w", encoding="utf-8")],
                    level=10, format="[%(levelname)s] %(filename)s %(funcName)s %(asctime)s %(message)s")
log = logging.getLogger(__name__)


class UnsupportedFormatError(Exception):
    def __str__(self):
        return "Unsupported file type\n不支持的文件格式"


def dumpfile(file_path, output_dir):
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s: s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]

    with open(file_path, 'rb') as f:
        header = f.read(8)
        assert binascii.b2a_hex(header) == b'4354454e4644414d'
        f.seek(2, 1)
        key_length = struct.unpack('<I', f.read(4))[0]
        key_data = bytearray(f.read(key_length))
        key_data = bytes(bytearray([byte ^ 0x64 for byte in key_data]))
        cryptor = AES.new(core_key, AES.MODE_ECB)
        key_data = unpad(cryptor.decrypt(key_data))[17:]
        key_length = len(key_data)

        key_data = bytearray(key_data)
        key_box = bytearray(range(256))
        c = 0
        last_byte = 0
        key_pos = 0
        for i in range(256):
            c = (key_box[i] + last_byte + key_data[key_pos]) & 0xff
            key_pos += 1
            if key_pos >= key_length:
                key_pos = 0
            key_box[i], key_box[c] = key_box[c], key_box[i]
            last_byte = c

        meta_length = struct.unpack('<I', f.read(4))[0]
        meta_data = bytearray(f.read(meta_length))
        meta_data = bytes(bytearray([byte ^ 0x63 for byte in meta_data]))
        meta_data = base64.b64decode(meta_data[22:])
        cryptor = AES.new(meta_key, AES.MODE_ECB)
        meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')
        meta_data = json.loads(meta_data[6:])

        crc32 = f.read(4)
        crc32 = struct.unpack('<I', bytes(crc32))[0]
        f.seek(5, 1)
        image_size = struct.unpack('<I', f.read(4))[0]
        image_data = f.read(image_size)

        file_name = os.path.splitext(os.path.basename(file_path))[0] + '.' + meta_data['format']
        music_path = os.path.join(output_dir, file_name)

        with open(music_path, 'wb') as m:
            chunk = bytearray()
            while True:
                chunk = bytearray(f.read(0x8000))
                chunk_length = len(chunk)
                if not chunk:
                    break
                for i in range(1, chunk_length + 1):
                    j = i & 0xff
                    chunk[i - 1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
                m.write(chunk)

    try:
        # Add tags
        if meta_data['format'] == 'flac':
            audio = flac.FLAC(music_path)
            audio.clear_pictures()
            image = flac.Picture()
            image.type = 3
            image.mime = 'image/jpeg'
            image.data = image_data
            audio.add_picture(image)

            # Add metadata
            audio['title'] = meta_data['musicName']
            audio['album'] = meta_data['album']
            audio['artist'] = '/'.join([artist[0] for artist in meta_data['artist']])

        elif meta_data['format'] == 'mp3':
            # Add album art
            audio = MP3(music_path, ID3=ID3)
            audio.tags.add(
                APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=image_data
                )
            )
            audio.save()

            # Add metadata
            audio = EasyID3(music_path)
            audio['title'] = meta_data['musicName']
            audio['album'] = meta_data['album']
            audio['artist'] = '/'.join([artist[0] for artist in meta_data['artist']])
        else:
            raise UnsupportedFormatError

        audio.save()
        log.info(f"已成功转换并添加音频元数据(Conversion successful with metadata added)"
                 f"： {os.path.basename(music_path)}")
    except Exception as err:
        log.error(f"在转换元数据时发生致命性错误(Fatal error occurred during metadata conversion)"
                  f"： {os.path.basename(music_path)}: {str(err)}")


def process_folder(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.ncm'):
            input_path = os.path.join(input_folder, file_name)
            try:
                dumpfile(input_path, output_folder)
                log.info(f"转换成功(Conversion successful)：{file_name}")
            except Exception as err:
                log.error(f"转换时发生致命性错误(Fatal error occurred during conversion)"
                          f"： {file_name}: {str(err)}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 ncm-converter.py INPUT_FOLDER [OUTPUT_FOLDER]\n"
              "Warning：If you wanna GUI mode, please run "
              "\npython3 main.py\n"
              "except run 'python3 ncm-convert.py"
              "\n如果希望使用图形用户界面，请使用"
              "\npython3 main.py"
              "\n而不是'python3 ncm-convert.py'")
        sys.exit(1)

    input_folder = sys.argv[1]

    if len(sys.argv) == 3:
        output_folder = sys.argv[2]
    else:
        output_folder = os.getcwd()  # Current working directory

    if not os.path.isdir(input_folder):
        log.error(f"错误(Error): {input_folder} is not a valid directory（找不到目录）")
        sys.exit(1)

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            log.info(f"创建输出目录(Created output directory): {output_folder}")
        except Exception as e:
            log.error(f"无法创建输出目录(Error creating output directory): {output_folder}: {str(e)}")
            sys.exit(1)

    log.info(f"输入目录(Input Folder): {input_folder}")
    log.info(f"输出目录(Output Folder): {output_folder}")

    process_folder(input_folder, output_folder)
    log.info("转换已全部完成（Conversion complete!）")

# 在代码末尾添加GPL兼容性声明（可选但推荐）
__license__ = "GPL-3.0-or-later"
