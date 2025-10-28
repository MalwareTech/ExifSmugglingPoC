# Exif Smuggling
A Proof-of-Concept evolution of Cache Smuggling. This attack conceals an executable payload inside a JPG's Exif data. As a result, image caching (such as that of a Web Browser) can be used to passively download the payload.

As a result, the example loader (`chrome_poc.ps1`) does not need to make any internet requests to fetch the second stage payload.
Instead, it simply extracts it from the Chrome browser's cache.

For full details see: [https://malwaretech.com/2025/10/exif-smuggling](https://malwaretech.com/2025/10/exif-smuggling.html)

## Example Usage
### Convert PowerShell Loader to ClickFix Command
`python3 build_clickfix_cmd.py --input-file chrome_poc.ps1 --output-file encoded_command.txt --fake-path "C:\test\doc.txt"`

### Embed payload dll inside arbitrary JPG
`python3 exif_smuggling.py --input-file image.jpg --output-file payload.jpg --payload hello_world.dll`

### Example Phishing page
`/www/index.html`
