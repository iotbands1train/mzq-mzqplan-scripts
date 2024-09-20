$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services"
$destinationPath = "Z:\001-MZQ Compliance Services"

# Create the destination directory if it doesn't exist
if (-not (Test-Path $destinationPath)) {
    New-Item -ItemType Directory -Force -Path $destinationPath
}

# Get all files from the source directory
$files = Get-ChildItem -Path $sourcePath -Recurse -File

$totalFiles = $files.Count
$progressCount = 0

# Function to copy files with progress
function Copy-Files {
    param (
        [string]$sourceFile,
        [string]$destinationFile,
        [ref]$progressCount
    )
    
    # Buffer size set to 1MB for optimized copy speed
    $bufferSize = 1MB
    $fileStreamSource = [System.IO.File]::OpenRead($sourceFile)
    $fileStreamDestination = [System.IO.File]::Create($destinationFile)

    try {
        $buffer = New-Object byte[] $bufferSize
        $bytesRead = 0
        
        while (($bytesRead = $fileStreamSource.Read($buffer, 0, $buffer.Length)) -gt 0) {
            $fileStreamDestination.Write($buffer, 0, $bytesRead)
        }
    }
    finally {
        $fileStreamSource.Close()
        $fileStreamDestination.Close()
    }

    # Update progress
    $progressCount.Value++
    Write-Progress -Activity "Copying files" -Status "$($progressCount.Value) of $totalFiles complete" -PercentComplete (($progressCount.Value / $totalFiles) * 100)
}

# Track jobs
$jobs = @()

# Copy files in parallel using jobs
foreach ($file in $files) {
    $destinationFile = $file.FullName.Replace($sourcePath, $destinationPath)
    $destinationDirectory = [System.IO.Path]::GetDirectoryName($destinationFile)
    
    if (-not (Test-Path $destinationDirectory)) {
        New-Item -ItemType Directory -Force -Path $destinationDirectory
    }

    # Start a job for each file copy
    $job = Start-Job -ScriptBlock {
        param ($src, $dst, $progressCount)
        Copy-Files -sourceFile $src -destinationFile $dst -progressCount $progressCount
    } -ArgumentList $file.FullName, $destinationFile, [ref]$progressCount

    $jobs += $job
}

# Wait for all jobs to complete
$jobs | ForEach-Object { 
    $null = Wait-Job -Job $_
    Remove-Job -Job $_
}

Write-Host "File copy completed!"
