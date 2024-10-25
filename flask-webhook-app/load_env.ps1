# Load environment variables from .env file
Get-Content .env | ForEach-Object {
    if ($_ -match "(.+?)=(.+)") {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        # Set the environment variable temporarily for the current session using Set-Item
        Set-Item -Path Env:$name -Value $value
    }
}
