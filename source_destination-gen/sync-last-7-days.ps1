# Set the source and destination paths
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
$destinationPath = "E:\test"

# Get the date 7 days ago (without time)
$sevenDaysAgo = (Get-Date).AddDays(-7).Date

# Get all files and directories that were created or modified in the last 7 days
$recentItems = Get-ChildItem -Path $sourcePath -Recurse | Where-Object { $_.LastWriteTime.Date -ge $sevenDaysAgo }

# Sync only the new or changed files to the destination
if ($recentItems) {
    foreach ($item in $recentItems) {
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
    Write-Output "No new or changed items found in the last 7 days to sync."
}
