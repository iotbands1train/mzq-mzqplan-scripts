<#
.SYNOPSIS
    This script maximizes the speed of folder synchronization from a source directory to a destination directory using robocopy.
.DESCRIPTION
    The script mirrors the content of the source directory to the destination directory, 
    utilizing multi-threading and optimized robocopy settings for faster execution.
.PARAMETER sourceDir
    The path to the source directory that needs to be synced.
.PARAMETER destinationDir
    The path to the destination directory where the files will be copied.
.NOTES
    Author: [Your Name]
    Date: [Today's Date]
    Version: 1.1
#>

# Define the source directory path
$sourceDir = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"

# Define the destination directory path
$destinationDir = "E:\test"

# Multi-line comment
# This block checks if the destination directory exists.
# If it doesn't exist, it creates the directory.
if (-not (Test-Path $destinationDir)) {
    # Create the destination directory
    New-Item -Path $destinationDir -ItemType Directory
}

# Define the log file path for robocopy operation (can be minimized or removed for speed)
$logFile = "C:\s3synclogs\sync-folders.log"

# Single-line comment
# Sync the folders using robocopy with multi-threading and optimized settings for maximum speed
robocopy $sourceDir $destinationDir /MIR /MT:32 /R:1 /W:1 /LOG:$logFile

# Capture the exit code of robocopy
$exitCode = $LASTEXITCODE

# Multi-line comment
# This block checks the robocopy exit code.
# If the exit code indicates an error (8 or higher), it logs an error message.
# Otherwise, it outputs a success message.
if ($exitCode -ge 8) {
    # Log an error message if robocopy encountered an issue
    Write-Error "Robocopy encountered an error with exit code $exitCode. Please check the log file for more details."
} else {
    # Output a success message if the sync operation was successful
    Write-Output "Sync completed successfully with exit code $exitCode."
}
