# Set the local and S3 paths
$localPath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
$s3Path = "s3://mzq-mzqplan-s3bucket/mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/"

# Step 1: Get the list of files in the local directory
Write-Output "Fetching the list of files from the local directory..."
$localFiles = Get-ChildItem -Path $localPath -Recurse -File | ForEach-Object {
    $_.FullName.Replace($localPath, "").Replace("\", "/").TrimStart("/")
}

Write-Output "Found $($localFiles.Count) files in the local directory."

# Step 2: Get the list of files in the S3 bucket using AWS CLI
Write-Output "Fetching the list of files from the S3 bucket..."
$s3Files = aws s3 ls $s3Path --recursive | ForEach-Object {
    $_.Split(' ')[-1]
}

Write-Output "Found $($s3Files.Count) files in the S3 bucket."

# Step 3: Use HashSet for faster lookup
Write-Output "Initializing HashSets for comparison..."
$localFileSet = [System.Collections.Generic.HashSet[string]]::new()
$s3FileSet = [System.Collections.Generic.HashSet[string]]::new()

# Add local files to HashSet
foreach ($file in $localFiles) {
    $null = $localFileSet.Add($file)
}

# Add S3 files to HashSet
foreach ($file in $s3Files) {
    $null = $s3FileSet.Add($file)
}

# Step 4: Find files that are in the local directory but not in S3
$localOnly = $localFileSet | Where-Object { -not $s3FileSet.Contains($_) }

# Step 5: Find files that are in S3 but not in the local directory
$s3Only = $s3FileSet | Where-Object { -not $localFileSet.Contains($_) }

# Step 6: Output the differences
Write-Output "Comparison complete. Results:"

if ($localOnly.Count -gt 0) {
    Write-Output "Files in the local directory but not in S3:"
    $localOnly | ForEach-Object { Write-Output $_ }
} else {
    Write-Output "No files in the local directory that are missing in S3."
}

if ($s3Only.Count -gt 0) {
    Write-Output "Files in S3 but not in the local directory:"
    $s3Only | ForEach-Object { Write-Output $_ }
} else {
    Write-Output "No files in S3 that are missing in the local directory."
}
