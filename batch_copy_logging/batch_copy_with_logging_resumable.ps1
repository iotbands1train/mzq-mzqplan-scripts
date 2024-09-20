# Define source and destination paths
$sourceDir = "C:\Users\Administrator\Box\001-MZQ Compliance Services\_Wrapper\Generated Wraps"
$destDir = "E:\waitlisted2"

# Define log file path and state file path
$logFile = "D:\logs\copywrappertest\copy.log"
$stateFile = "D:\logs\copywrappertest\copy_state.json"

function Log-Message {
    param (
        [string]$title,
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $fullMessage = "[$timestamp] $title : $message"
    Add-Content -Path $logFile -Value $fullMessage
    Write-Output $fullMessage
}

function Load-State {
    if (Test-Path -Path $stateFile) {
        $state = Get-Content -Path $stateFile | ConvertFrom-Json
        return $state
    }
    return @{}
}

function Save-State {
    param (
        [hashtable]$state
    )
    $state | ConvertTo-Json | Set-Content -Path $stateFile
}

function Copy-FilesInBatches {
    param (
        [string]$src,
        [string]$dest,
        [int]$batchSize = 5
    )
    if (-not (Test-Path -Path $dest)) {
        New-Item -ItemType Directory -Path $dest
    }

    $state = Load-State
    $allItems = Get-ChildItem -Path $src -Recurse
    $remainingItems = $allItems | Where-Object { $_.FullName -notin $state.Keys }

    $batches = @()
    for ($i = 0; $i -lt $remainingItems.Count; $i += $batchSize) {
        $batches += ,@($remainingItems[$i..([math]::Min($i + $batchSize - 1, $remainingItems.Count - 1))])
    }

    $jobs = @()
    for ($batchNumber = 1; $batchNumber -le $batches.Count; $batchNumber++) {
        $batch = $batches[$batchNumber - 1]
        $job = Start-Job -ScriptBlock {
            param ($batch, $src, $dest, $stateFile)
            function Load-State {
                if (Test-Path -Path $stateFile) {
                    $state = Get-Content -Path $stateFile | ConvertFrom-Json
                    return $state
                }
                return @{}
            }
            function Save-State {
                param (
                    [hashtable]$state
                )
                $state | ConvertTo-Json | Set-Content -Path $stateFile
            }
            $state = Load-State
            foreach ($item in $batch) {
                $s = $item.FullName
                $d = Join-Path -Path $dest -ChildPath (Resolve-Path -Path (Join-Path -Path $dest -ChildPath ($item.FullName.Substring($src.Length))))
                if ($item.PSIsContainer) {
                    if (-not (Test-Path -Path $d)) {
                        Copy-Item -Path $s -Destination $d -Recurse
                    }
                } else {
                    if (-not (Test-Path -Path $d -PathType Leaf)) {
                        $dir = Split-Path -Path $d -Parent
                        if (-not (Test-Path -Path $dir)) {
                            New-Item -ItemType Directory -Path $dir
                        }
                        Copy-Item -Path $s -Destination $d
                    }
                }
                # Update state file after copying each item
                $state[$s] = $true
                Save-State -state $state
            }
        } -ArgumentList $batch, $src, $dest, $stateFile
        $jobs += $job
        Log-Message -title "INFO" -message "Started batch job $batchNumber"
    }

    $jobs | ForEach-Object { Receive-Job -Job $_ -Wait }
}

# Record start time
$startTime = Get-Date
Log-Message -title "INFO" -message "Copy started at: $startTime"

# Perform the copy operation in batches
Copy-FilesInBatches -src $sourceDir -dest $destDir -batchSize 5

# Record end time
$endTime = Get-Date
Log-Message -title "INFO" -message "Copy completed at: $endTime"

# Calculate and log time elapsed
$timeElapsed = $endTime - $startTime
Log-Message -title "INFO" -message "Time elapsed: $timeElapsed"

Write-Output "Copy completed. Check the log file at $logFile for details."
