# Start servers for PWA testing
$apiPort = 8000
$htmlPort = 8080

# Function to check if a port is available
function Test-TcpConnection {
    param (
        [string]$ComputerName = "localhost",
        [int]$Port
    )
    
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $connection = $tcpClient.BeginConnect($ComputerName, $Port, $null, $null)
        $wait = $connection.AsyncWaitHandle.WaitOne(100)
        
        if ($wait) {
            $tcpClient.EndConnect($connection)
            return $true
        }
        else {
            return $false
        }
    }
    catch {
        return $false
    }
    finally {
        if ($tcpClient) {
            $tcpClient.Close()
        }
    }
}

# Check if API server is already running
$apiRunning = Test-TcpConnection -Port $apiPort
Write-Host "API Server on port $apiPort is running: $apiRunning"
if ($flaskInstalled.Trim() -eq "False") {
    Write-Host "Installing Flask for PWA server..."
    pip install flask
}

# Start API server if not running
if (-not $apiRunning) {
    Write-Host "Starting API server on port $apiPort..."
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "$apiPort" -WorkingDirectory "j:/FG1/workspace/empty/a1"
    Start-Sleep -Seconds 2
    $apiRunning = Test-TcpConnection -Port $apiPort
    Write-Host "API Server started successfully: $apiRunning"
}

# Check if HTML server is already running
$htmlRunning = Test-TcpConnection -Port $htmlPort
Write-Host "PWA Server on port $htmlPort is running: $htmlRunning"

# Start PWA HTTP server if not running
if (-not $htmlRunning) {
    Write-Host "Starting PWA server on port $htmlPort..."
    Start-Process -NoNewWindow -FilePath "python" -ArgumentList "new-ui/pwa_http_server.py" -WorkingDirectory "j:/FG1/workspace/empty/a1"
    Start-Sleep -Seconds 2
    $htmlRunning = Test-TcpConnection -Port $htmlPort
    Write-Host "PWA Server started successfully: $htmlRunning"
}

Write-Host "Servers started! Access your PWA at: http://localhost:$htmlPort"
Write-Host "API server is available at: http://localhost:$apiPort"
Write-Host "Press Ctrl+C to stop the servers when done."
