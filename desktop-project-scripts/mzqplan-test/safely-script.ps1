# Define the source and destination paths
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.xlsm"
$sourcePath = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Wrap Portal Login Generator_3.xlsm"
$destinationPath = "E:\excel"

# Function to safely copy file
function SafeCopy-File {
    param (
        [string]$src,
        [string]$dest
    )
    
    # Check if the source file exists
    if (Test-Path $src) {
        # Create the destination directory if it does not exist
        if (-not (Test-Path $dest)) {
            try {
                New-Item -Path $dest -ItemType Directory -ErrorAction Stop
                Write-Output "Created destination directory: $dest"
            } catch {
                Write-Error "Failed to create destination directory: $dest. Error: $_"
                exit 1
            }
        }

        # Define the full destination file path
        $destFilePath = Join-Path -Path $dest -ChildPath (Split-Path -Leaf $src)

        # Copy the file with error handling
        try {
            Copy-Item -Path $src -Destination $destFilePath -Force -ErrorAction Stop
            Write-Output "File copied successfully from $src to $destFilePath"
        } catch {
            Write-Error "Failed to copy file from $src to $destFilePath. Error: $_"
        }
    } else {
        Write-Error "Source file does not exist: $src"
    }
}

# Call the function to copy the file
SafeCopy-File -src $sourcePath -dest $destinationPath
