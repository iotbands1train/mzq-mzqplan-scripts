# Set the source and destination paths
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
$destinationPath = "E:\test"

# Get yesterday's date (without time)
$yesterday = (Get-Date).AddDays(-1).Date

# Get all files and directories that were created or modified yesterday
$yesterdayItems = Get-ChildItem -Path $sourcePath -Recurse | Where-Object { $_.LastWriteTime.Date -eq $yesterday }

# Sync only the new or changed files to the destination
if ($yesterdayItems) {
    foreach ($item in $yesterdayItems) {
        $destination = $item.FullName.Replace($sourcePath, $destinationPath)
        
        # Ensure the destination directory exists
        $destDir = [System.IO.Path]::GetDirectoryName($destination)
        if (-not (Test-Path $destDir)) {
            New-Item -Path $destDir -ItemType Directory -Force
        }

        # Copy the file or directory
        Copy-Item -Path $item.FullName -Destination $destination -Force
        Write-Output "Synced: $($item.FullName) to $destination"
    }
} else {
    Write-Output "No new or changed items found for yesterday to sync."
}
