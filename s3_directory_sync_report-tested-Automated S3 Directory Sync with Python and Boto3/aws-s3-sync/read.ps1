# Define the source and destination directories
$sourceDir = "E:\clients-test"
$destDir = "E:\MZQPlans-prod\javascripts\clients"

# Get all directories that do not start with an underscore
$foldersToCopy = Get-ChildItem -Path $sourceDir -Directory | Where-Object { $_.Name -notmatch "^_" }

# Copy each folder to the destination directory
foreach ($folder in $foldersToCopy) {
    $sourceFolderPath = Join-Path -Path $sourceDir -ChildPath $folder.Name
    $destFolderPath = Join-Path -Path $destDir -ChildPath $folder.Name
    Copy-Item -Path $sourceFolderPath -Destination $destFolderPath -Recurse -Force
}

Write-Output "Folders copied successfully."
