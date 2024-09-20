# Define the path to the cache directory
$cachePath = "C:\Users\Administrator\AppData\Local\Box\Box\cache"

# Define the maximum number of items allowed
$maxItems = 20

# Count the number of items in the cache directory
$itemCount = (Get-ChildItem -Path $cachePath -Recurse | Measure-Object).Count

# Check if the item count exceeds the maximum allowed
if ($itemCount -gt $maxItems) {
    # Log an event to the Windows Event Log
    $eventMessage = "Cache directory contains more than $maxItems items. Current count: $itemCount"
    Write-EventLog -LogName Application -Source "BoxCacheMonitor" -EventID 1001 -EntryType Information -Message $eventMessage
}
