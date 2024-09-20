# PowerShell script to install NetSharp

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

Log-Message "Starting NetSharp installation script."

# Install Chocolatey if not installed
if (-not (Get-Command choco.exe -ErrorAction SilentlyContinue)) {
    Log-Message "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Start-Sleep -Seconds 30
}

# Install NetSharp (assuming it's available via Chocolatey or download manually if not)
Log-Message "Installing NetSharp..."
# If NetSharp is available via Chocolatey
choco install netsharp -y
# Else, download and install manually
# Invoke-WebRequest -Uri "https://download.link/to/netsharp-installer.exe" -OutFile "C:\Temp\netsharp-installer.exe"
# Start-Process "C:\Temp\netsharp-installer.exe" -ArgumentList "/silent" -Wait

Log-Message "NetSharp installation script completed."
