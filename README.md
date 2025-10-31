# ⚡ IENDLoader

**Hide .NET payloads in PNG images**

Hides .NET payloads in PNG images by embedding the payload in the `iend` chunk, which is a part of the PNG standard. The payload is compressed and encoded with Base64. The resulting image can be used to execute payloads by extracting the payload and executing it with .NET reflection. This is achieved by using the .NET method `Assembly.Load` to load the payload assembly and execute its main method. 
---

## Quick Start

### Run from Source
```bash
pip install customtkinter
python3 iendloader.py
```

### Build Standalone EXE 
```bash
pip install customtkinter pyinstaller

# Windows ARM64
pyinstaller build_windows_arm64.spec

# Windows x64
pyinstaller build_windows.spec


```

**Output:** `dist/IENDLoader.exe`

---

## 📖 How to Use

1. **Select Payload** - Choose .NET assembly (.exe)
2. **Select Image** - Select horse.png in images folder or select your own
3. **Embed** - Creates weaponized image
4. **Entry Point** - Toggle auto-discovery or enter manually (e.g., `Client.Program.Main`)
5. **Enter URL** - Where you'll host the image
6. **Generate** - Click "Generate PowerShell One-Liner"
7. **Copy** - Copy command to clipboard
8. **Execute** - Run on target Windows machine

### Host the Image for local testing
```bash
# Navigate to images folder
cd images

python3 -m http.server 8080
```

### Entry Point Examples
- Auto-discovery (default) - finds Main() automatically (may not work for all payloads especially if obfuscated)
- Manual: `Client.Program.Main` (AsyncRAT/Quasar)
- Manual: `Program.Main` (simple apps)

---

## ⚠️ Educational Use Only

Authorized testing in lab environments only. Don't be stupid.


