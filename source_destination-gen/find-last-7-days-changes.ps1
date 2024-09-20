# Set the source path to monitor
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"

# Get the date 7 days ago (without time)
$sevenDaysAgo = (Get-Date).AddDays(-7).Date

# Get all files and directories that were created or modified in the last 7 days
$recentItems = Get-ChildItem -Path $sourcePath -Recurse | Where-Object { $_.LastWriteTime.Date -ge $sevenDaysAgo }

# Check if there are any items found
if ($recentItems) {
    Write-Output "Items created or modified in the last 7 days:"
    foreach ($item in $recentItems) {
        $logEntry = "{0} - Item: {1}" -f (Get-Date), $item.FullName
        Write-Output $logEntry
    }
} else {
    Write-Output "No new or changed items found in the last 7 days."
}
