# Define the path to the cache directory
$cachePath = "C:\Users\Administrator\AppData\Local\Box\Box\cache"
$numb=100
# Check if the directory exists
if (Test-Path $cachePath) {
    # Count the number of items in the cache directory
    $itemCount = (Get-ChildItem -Path $cachePath -Recurse -Force | Measure-Object).Count

    # If the number of items is greater than 200, run the deletion script
    if ($itemCount -gt $numb) {
        # Get all files and directories in the cache directory
        $items = Get-ChildItem -Path $cachePath -Recurse -Force

        # Attempt to delete each item
        foreach ($item in $items) {
            try {
                Remove-Item -Path $item.FullName -Force -Recurse -ErrorAction Stop
                Write-Output "Deleted: $($item.FullName)"
            } catch {
                Write-Output "Skipped: $($item.FullName) - $_"
            }
        }

        # Attempt to delete the cache directory itself
        try {
            Remove-Item -Path $cachePath -Force -Recurse -ErrorAction Stop
            Write-Output "Deleted cache directory: $cachePath"
        } catch {
            Write-Output "Failed to delete cache directory: $cachePath - $_"
        }
    } else {
        Write-Output "The cache directory has $itemCount items, which is not more than $numb."
    }
} else {
    Write-Output "Cache directory does not exist."
}
