# Set the source and destination paths
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
$destinationPath = "E:\test"

# Get today's date (without time)
$today = (Get-Date).Date

# Get all files and directories that were created or modified today
$todayItems = Get-ChildItem -Path $sourcePath -Recurse | Where-Object { $_.LastWriteTime.Date -eq $today }

# Sync only the new or changed files to the destination
if ($todayItems) {
    foreach ($item in $todayItems) {
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
    Write-Output "No new or changed items found for today to sync."
}
