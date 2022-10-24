pyinstaller -F -n SUDA-Net-Daemon -i resources\suda-logo.png -p dist .\daemon.py
COPY configurations.json dist\configurations.json
COPY chromedriver.exe dist\chromedriver.exe
$compress = @{
    Path = "configurations.json", "chromedriver.exe", "dist\SUDA-Net-Daemon.exe"
    CompressionLevel = "Fastest"
    DestinationPath = "dist\SUDA-Net-Daemon-v0.2.zip"
}
Compress-Archive @compress -Force