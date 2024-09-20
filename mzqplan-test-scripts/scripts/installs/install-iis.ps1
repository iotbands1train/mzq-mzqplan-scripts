#install-iis.ps1

# PowerShell script to install IIS and configure IIS Manager

# Enable script execution
Set-ExecutionPolicy Unrestricted -Force

# Function to log messages
function Log-Message {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "$timestamp - $message"
}

Log-Message "Starting IIS installation script."

# Install IIS
Log-Message "Installing IIS..."
Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Start IIS service
Log-Message "Starting IIS service..."
Start-Service W3SVC

# Reboot and wait
Log-Message "Rebooting system to complete IIS installation..."
Restart-Computer -Force

# Wait for system to reboot
Start-Sleep -Seconds 120

Log-Message "IIS installation script completed."
