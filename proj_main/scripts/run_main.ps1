# Define the path to the config file
$logPath = 'D:\logs\proj_main_scripts_run_main_ps1\sync_wrap-gen.logs' 

# Function to log messages
function Write-Log {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $message" | Out-File -Append -FilePath $logPath
}

# Function to read the config file and convert it to a dictionary
function Get-Config {
    param (
        [string]$Path
    )
    $config = @{}
    Get-Content -Path $Path | ForEach-Object {
        if ($_ -match '^\[DEFAULT\]') {
            # Skip the section header
        } elseif ($_ -match '^\s*#') {
            # Skip comments
        } elseif ($_ -match '^\s*$') {
            # Skip empty lines
        } else {
            $name, $value = $_ -split '=', 2
            $config[$name.Trim()] = $value.Trim()
        }
    }
    return $config
}

try {
    Write-Log "Starting script execution."
    
    # Load the configuration
    $configPath = 'D:\proj_main\settings\config.properties' # Ensure this path is defined or passed as a parameter
    $config = Get-Config -Path $configPath
    Write-Log "Loaded configuration from $configPath."

    # Define the path to the Python executable and the main.py script
    $pythonPath = $config['python_path']
    $scriptPath = "D:\proj_main\codes\main.py"
    & $pythonPath $scriptPath

    Write-Log "Python script execution completed."

    # Run additional Python scripts
    $scriptPath2 = "D:\proj_main\codes\wrapper_gen_xlm_to_csv.py" 
    & $pythonPath $scriptPath2

    $scriptPath3 = "D:\proj_main_livegen\upload_to_s3_project\src\main.py" 
    & $pythonPath $scriptPath3

    $scriptPath4 = "D:\other-code-files\download_file_wrap copy.py" 
    & $pythonPath $scriptPath4

} catch {
    Write-Log "An error occurred: $_"
}
