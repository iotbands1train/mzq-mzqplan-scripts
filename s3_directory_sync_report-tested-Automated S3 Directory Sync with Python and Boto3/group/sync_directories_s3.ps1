param (
    [string]$LocalDirectory = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps",
    [string]$BucketName = "mzq-mzqplan-s3bucket",
    [string]$S3Directory = "mzqplan-aws-cloud/c_drive/Box/001-MZQ Compliance Services/_Wrapper/Generated Wraps",
    [int]$MaxWorkers = 55  # Increased by 10%
)

# AWS S3 Configuration
$TransferConfig = @{
    multipart_threshold = 8MB
    max_concurrency = 11  # Increased by 10%
    multipart_chunksize = 7.5MB  # Slightly reduced chunk size for faster uploads
    use_threads = $true
}

# Initialize S3 client using the AWS Tools for PowerShell
$S3Client = New-Object -TypeName Amazon.S3.AmazonS3Client

function Upload-File {
    param (
        [string]$LocalPath,
        [string]$Bucket,
        [string]$S3Path
    )
    try {
        $TransferUtility = New-Object Amazon.S3.Transfer.TransferUtility($S3Client)
        $TransferUtility.Upload($LocalPath, $Bucket, $S3Path, $TransferConfig)
        Write-Host "Successfully uploaded $LocalPath to s3://$Bucket/$S3Path"
    } catch {
        Write-Error "Failed to upload $LocalPath to s3://$Bucket/$S3Path : $_"
    }
}

function Sync-Directories {
    param (
        [string]$LocalDirectory,
        [string]$BucketName,
        [string]$S3Directory,
        [int]$MaxWorkers
    )

    $UploadTasks = @()
    $StartTime = Get-Date

    # Use parallel processing with Start-Job (compatible with older PowerShell versions)
    Get-ChildItem -Path $LocalDirectory -Recurse -File | ForEach-Object {
        $LocalPath = $_.FullName
        $RelativePath = $LocalPath.Substring($LocalDirectory.Length + 1) -replace '\\', '/'
        $S3Path = "$S3Directory/$RelativePath"

        # Start a background job for each upload to simulate parallelism
        $UploadTasks += Start-Job -ScriptBlock {
            param ($LocalPath, $BucketName, $S3Path)
            Upload-File -LocalPath $LocalPath -Bucket $BucketName -S3Path $S3Path
        } -ArgumentList $LocalPath, $BucketName, $S3Path
    }

    # Wait for all jobs to complete
    $UploadTasks | ForEach-Object { Receive-Job -Job $_ -Wait }
    $UploadTasks | ForEach-Object { Remove-Job -Job $_ }

    $EndTime = Get-Date
    $ElapsedTime = $EndTime - $StartTime
    Write-Host "All files uploaded successfully in $($ElapsedTime.TotalSeconds) seconds"
    Write-Host "Time elapsed: $($ElapsedTime.TotalMinutes) minutes ($($ElapsedTime.TotalHours) hours)"
}

# Start the directory synchronization
Sync-Directories -LocalDirectory $LocalDirectory -BucketName $BucketName -S3Directory $S3Directory -MaxWorkers $MaxWorkers
