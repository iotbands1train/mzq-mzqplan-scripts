# Set the path to monitor
$directoryPath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"

# Get today's date (without time)
$today = (Get-Date).Date

# Get all files and directories that were created or modified today
$todayItems = Get-ChildItem -Path $directoryPath -Recurse | Where-Object { $_.LastWriteTime.Date -eq $today }

# Check if there are any new or modified items today
if ($todayItems) {
    Write-Output "New or changed items today:"
    $todayItems | ForEach-Object {
        $logEntry = "{0} - Item: {1}" -f (Get-Date), $_.FullName
        Write-Output $logEntry
    }
} else {
    Write-Output "No new or changed items found for today."
}
