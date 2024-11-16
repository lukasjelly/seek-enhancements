# Load environment variables from .env file
$envFilePath = ".env"
if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath
    foreach ($line in $envContent) {
        if ($line -match "^\s*([^#\s]+?)\s*=\s*(.+?)\s*$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
} else {
    Write-Error "The .env file does not exist."
    exit 1
}

# Use the credentials to create models
$DB_NAME = $env:DB_NAME
$DB_HOST = $env:DB_HOST
$DB_USER = $env:DB_USER
$DB_PORT = $env:DB_PORT
$DB_PASSWORD = $env:DB_PASSWORD

if ($null -eq $DB_NAME -or $null -eq $DB_HOST -or $null -eq $DB_USER -or $null -eq $DB_PORT -or $null -eq $DB_PASSWORD) {
    Write-Error "One or more environment variables are missing."
    exit 1
}

# Run sequelize-auto command with TypeScript output
$command = "sequelize-auto -o './src/models' -d $DB_NAME -h $DB_HOST -u $DB_USER -p $DB_PORT -x $DB_PASSWORD -e mysql -l ts --cm p --cp c"
Invoke-Expression $command