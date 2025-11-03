using System;
using System.Windows;

namespace IENDLoader
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            
            // Global exception handler
            AppDomain.CurrentDomain.UnhandledException += (sender, args) =>
            {
                var ex = args.ExceptionObject as Exception;
                MessageBox.Show($"Fatal error: {ex?.Message}\n\nStack trace:\n{ex?.StackTrace}", 
                    "Application Error", MessageBoxButton.OK, MessageBoxImage.Error);
            };
            
            DispatcherUnhandledException += (sender, args) =>
            {
                MessageBox.Show($"Error: {args.Exception.Message}\n\nStack trace:\n{args.Exception.StackTrace}", 
                    "Application Error", MessageBoxButton.OK, MessageBoxImage.Error);
                args.Handled = true;
            };

            try
            {
                var w = new MainWindow();
                w.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString(), "Startup Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(-1);
            }
        }
    }
}
