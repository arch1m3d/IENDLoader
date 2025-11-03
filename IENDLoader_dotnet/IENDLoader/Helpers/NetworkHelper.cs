using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace IENDLoader.Helpers
{
    /// <summary>
    /// Helper class for network-related operations
    /// </summary>
    public static class NetworkHelper
    {
        /// <summary>
        /// Gets the local IP address of the machine
        /// </summary>
        public static string GetLocalIpAddress()
        {
            try
            {
                using var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, 0);
                socket.Connect("8.8.8.8", 80);
                var endPoint = socket.LocalEndPoint as IPEndPoint;
                return endPoint?.Address.ToString() ?? "192.168.1.100";
            }
            catch
            {
                // Fallback: try to get from network interfaces
                try
                {
                    var host = Dns.GetHostEntry(Dns.GetHostName());
                    var localIp = host.AddressList
                        .FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
                    return localIp?.ToString() ?? "192.168.1.100";
                }
                catch
                {
                    return "192.168.1.100";
                }
            }
        }

        /// <summary>
        /// Generates a default hosting URL for the weaponized image
        /// </summary>
        public static string GenerateDefaultUrl(string filename, int port = 8080)
        {
            string localIp = GetLocalIpAddress();
            return $"http://{localIp}:{port}/{filename}";
        }
    }
}
