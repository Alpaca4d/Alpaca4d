using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Eto;
using Eto.Forms;
using Eto.Drawing;
using System.Reflection;
using System.Diagnostics;

namespace Alpaca4d.Gh.Forms
{
    public partial class Advertise
    {
        public static int NumberOfElements = 10;

        public Advertise()
        {
            var windows = new Eto.Forms.Form();
            windows.Size = new Eto.Drawing.Size(800, 450);
            windows.Maximizable = false;
            windows.Minimizable = false;
            windows.Resizable = false;
            windows.Padding = new Eto.Drawing.Padding(5, 5, 5, 5);
            windows.BackgroundColor = new Eto.Drawing.Color(1, 1, 1);

            var centerScreen = Eto.Forms.Screen.DisplayBounds.Center;
            windows.Location = new Eto.Drawing.Point((int)centerScreen.X - windows.Size.Width / 2, (int)centerScreen.Y - windows.Size.Height / 2);
            windows.Icon = Eto.Drawing.Icon.FromResource("Alpaca4d.Gh.Resources.Tab.png");
            
            var imageView = new Eto.Forms.ImageView();
            imageView.Image = Eto.Drawing.Bitmap.FromResource("Alpaca4d.Gh.Resources.Sponsors.become a sponsor.png");

            windows.Content = imageView;
            windows.Show();
        }

        public static Advertise Default()
        {
            return new Advertise();
        }
    }

    /// <summary>
    /// Enhanced Eto Form with buttons, images, text, and link functionality
    /// </summary>
    public class InteractiveForm : Form
    {
        private const string SUPPORT_EMAIL = "support@alpaca4d.com";
        private const string WEBSITE_URL = "https://alpaca4d.com";
        private const string GITHUB_URL = "https://github.com/Alpaca4d/Alpaca4d";

        public InteractiveForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            // Form properties
            Title = "Alpaca4d - Interactive Form";
            Size = new Size(600, 500);
            Maximizable = false;
            Minimizable = true;
            Resizable = false;
            Padding = new Padding(20);
            BackgroundColor = Eto.Drawing.Colors.White;

            // Center the form on screen
            var centerScreen = Screen.DisplayBounds.Center;
            Location = new Point((int)centerScreen.X - Size.Width / 2, (int)centerScreen.Y - Size.Height / 2);

            // Set icon if available
            try
            {
                Icon = Icon.FromResource("Alpaca4d.Gh.Resources.Tab.png");
            }
            catch
            {
                // Icon not found, continue without it
            }

            // Create main layout
            Content = CreateMainLayout();
        }

        private Control CreateMainLayout()
        {
            var layout = new TableLayout
            {
                Spacing = new Size(10, 10)
            };

            // Header section with logo and title
            layout.Rows.Add(CreateHeaderSection());

            // Main content section
            layout.Rows.Add(CreateContentSection());

            // Button section
            layout.Rows.Add(CreateButtonSection());

            // Footer section
            layout.Rows.Add(CreateFooterSection());

            return layout;
        }

        private Control CreateHeaderSection()
        {
            var headerLayout = new StackLayout
            {
                Orientation = Orientation.Vertical,
                HorizontalContentAlignment = HorizontalAlignment.Center,
                Spacing = 10
            };

            // Logo (if available)
            try
            {
                var logoView = new ImageView
                {
                    Image = Bitmap.FromResource("Alpaca4d.Gh.Resources.Logo.png"),
                    Size = new Size(100, 100)
                };
                headerLayout.Items.Add(logoView);
            }
            catch
            {
                // Logo not found, add placeholder
                var placeholderLabel = new Label
                {
                    Text = "🦙",
                    Font = new Font(SystemFont.Default, 48),
                    TextAlignment = TextAlignment.Center
                };
                headerLayout.Items.Add(placeholderLabel);
            }

            // Title
            var titleLabel = new Label
            {
                Text = "Welcome to Alpaca4d",
                Font = SystemFonts.Bold(18),
                TextAlignment = TextAlignment.Center,
                TextColor = Eto.Drawing.Colors.DarkBlue
            };
            headerLayout.Items.Add(titleLabel);

            // Subtitle
            var subtitleLabel = new Label
            {
                Text = "Structural Analysis for Grasshopper",
                Font = new Font(SystemFont.Default, 12),
                TextAlignment = TextAlignment.Center,
                TextColor = Eto.Drawing.Colors.Gray
            };
            headerLayout.Items.Add(subtitleLabel);

            return headerLayout;
        }

        private Control CreateContentSection()
        {
            var contentLayout = new StackLayout
            {
                Orientation = Orientation.Vertical,
                Spacing = 15
            };

            // Description text
            var descriptionLabel = new Label
            {
                Text = "Alpaca4d is a powerful structural analysis plugin for Grasshopper. " +
                       "Get support, contribute to development, or learn more about our features:",
                Wrap = WrapMode.Word,
                TextAlignment = TextAlignment.Left
            };
            contentLayout.Items.Add(descriptionLabel);

            // Feature list
            var featuresLabel = new Label
            {
                Text = "✓ Cross-platform compatibility\n" +
                       "✓ Advanced structural analysis\n" +
                       "✓ Integration with Grasshopper\n" +
                       "✓ Open source development",
                TextColor = Eto.Drawing.Colors.DarkGreen
            };
            contentLayout.Items.Add(featuresLabel);

            return contentLayout;
        }

        private Control CreateButtonSection()
        {
            var buttonLayout = new TableLayout
            {
                Spacing = new Size(10, 10)
            };

            // First row of buttons
            var row1 = new TableRow();
            row1.Cells.Add(CreateWebsiteButton());
            row1.Cells.Add(CreateGitHubButton());
            buttonLayout.Rows.Add(row1);

            // Second row of buttons
            var row2 = new TableRow();
            row2.Cells.Add(CreateSupportEmailButton());
            row2.Cells.Add(CreateDocumentationButton());
            buttonLayout.Rows.Add(row2);

            // Third row - Custom action button
            var row3 = new TableRow();
            row3.Cells.Add(CreateCustomActionButton());
            row3.Cells.Add(new TableCell()); // Empty cell
            buttonLayout.Rows.Add(row3);

            return buttonLayout;
        }

        private Button CreateWebsiteButton()
        {
            var button = new Button
            {
                Text = "🌐 Visit Website",
                Size = new Size(200, 40),
                BackgroundColor = Eto.Drawing.Colors.LightBlue
            };
            
            button.Click += (sender, e) => OpenUrl(WEBSITE_URL);
            return button;
        }

        private Button CreateGitHubButton()
        {
            var button = new Button
            {
                Text = "📂 GitHub Repository",
                Size = new Size(200, 40),
                BackgroundColor = Eto.Drawing.Colors.Silver
            };
            
            button.Click += (sender, e) => OpenUrl(GITHUB_URL);
            return button;
        }

        private Button CreateSupportEmailButton()
        {
            var button = new Button
            {
                Text = "📧 Contact Support",
                Size = new Size(200, 40),
                BackgroundColor = Eto.Drawing.Colors.LightGreen
            };
            
            button.Click += (sender, e) => SendEmail(SUPPORT_EMAIL, "Alpaca4d Support Request", "Hello,\n\nI need help with...");
            return button;
        }

        private Button CreateDocumentationButton()
        {
            var button = new Button
            {
                Text = "📖 Documentation",
                Size = new Size(200, 40),
                BackgroundColor = Eto.Drawing.Colors.LightYellow
            };
            
            button.Click += (sender, e) => OpenUrl("https://alpaca4d.com/docs");
            return button;
        }

        private Button CreateCustomActionButton()
        {
            var button = new Button
            {
                Text = "⚡ Custom Action",
                Size = new Size(200, 40),
                BackgroundColor = Eto.Drawing.Colors.LightCoral
            };
            
            button.Click += (sender, e) => ShowCustomDialog();
            return button;
        }

        private Control CreateFooterSection()
        {
            var footerLayout = new StackLayout
            {
                Orientation = Orientation.Horizontal,
                HorizontalContentAlignment = HorizontalAlignment.Center,
                Spacing = 20
            };

            // Version info
            var versionLabel = new Label
            {
                Text = $"Version: {GetAssemblyVersion()}",
                Font = new Font(SystemFont.Default, 9),
                TextColor = Eto.Drawing.Colors.Gray
            };
            footerLayout.Items.Add(versionLabel);

            // Close button
            var closeButton = new Button
            {
                Text = "Close",
                Size = new Size(80, 30)
            };
            closeButton.Click += (sender, e) => Close();
            footerLayout.Items.Add(closeButton);

            return footerLayout;
        }

        #region Helper Methods

        /// <summary>
        /// Opens a URL in the default web browser (cross-platform)
        /// </summary>
        private void OpenUrl(string url)
        {
            try
            {
                // Cross-platform URL opening
                var psi = new ProcessStartInfo
                {
                    FileName = url,
                    UseShellExecute = true
                };
                Process.Start(psi);
            }
            catch (Exception ex)
            {
                ShowErrorDialog($"Could not open URL: {ex.Message}");
            }
        }

        /// <summary>
        /// Opens the default email client with pre-filled email (cross-platform)
        /// </summary>
        private void SendEmail(string toEmail, string subject = "", string body = "")
        {
            try
            {
                var mailtoUrl = $"mailto:{toEmail}";
                if (!string.IsNullOrEmpty(subject) || !string.IsNullOrEmpty(body))
                {
                    mailtoUrl += "?";
                    if (!string.IsNullOrEmpty(subject))
                        mailtoUrl += $"subject={Uri.EscapeDataString(subject)}";
                    if (!string.IsNullOrEmpty(body))
                    {
                        if (!string.IsNullOrEmpty(subject))
                            mailtoUrl += "&";
                        mailtoUrl += $"body={Uri.EscapeDataString(body)}";
                    }
                }

                var psi = new ProcessStartInfo
                {
                    FileName = mailtoUrl,
                    UseShellExecute = true
                };
                Process.Start(psi);
            }
            catch (Exception ex)
            {
                ShowErrorDialog($"Could not open email client: {ex.Message}");
            }
        }

        /// <summary>
        /// Shows a custom dialog with more options
        /// </summary>
        private void ShowCustomDialog()
        {
            var dialog = new Dialog<bool>
            {
                Title = "Custom Action",
                Size = new Size(400, 200),
                Padding = new Padding(20)
            };

            var layout = new StackLayout
            {
                Orientation = Orientation.Vertical,
                Spacing = 15
            };

            layout.Items.Add(new Label 
            { 
                Text = "Choose an action:",
                Font = SystemFonts.Bold(12)
            });

            // Action buttons
            var actionLayout = new StackLayout
            {
                Orientation = Orientation.Horizontal,
                Spacing = 10
            };

            var action1Button = new Button { Text = "Open Examples" };
            action1Button.Click += (s, e) =>
            {
                dialog.Close(true);
                OpenUrl("https://github.com/Alpaca4d/Alpaca4d/tree/main/Examples");
            };

            var action2Button = new Button { Text = "Report Bug" };
            action2Button.Click += (s, e) =>
            {
                dialog.Close(true);
                SendEmail("bugs@alpaca4d.com", "Bug Report", "Describe the bug here...");
            };

            actionLayout.Items.Add(action1Button);
            actionLayout.Items.Add(action2Button);
            layout.Items.Add(actionLayout);

            // Cancel button
            var cancelButton = new Button { Text = "Cancel" };
            cancelButton.Click += (s, e) => dialog.Close(false);
            layout.Items.Add(cancelButton);

            dialog.Content = layout;
            dialog.ShowModal(this);
        }

        /// <summary>
        /// Shows an error dialog
        /// </summary>
        private void ShowErrorDialog(string message)
        {
            MessageBox.Show(this, message, "Error", MessageBoxType.Error);
        }

        /// <summary>
        /// Gets the assembly version
        /// </summary>
        private string GetAssemblyVersion()
        {
            try
            {
                return Assembly.GetExecutingAssembly().GetName().Version?.ToString() ?? "Unknown";
            }
            catch
            {
                return "Unknown";
            }
        }

        #endregion

        /// <summary>
        /// Static method to create and show the form
        /// </summary>
        public static void ShowForm()
        {
            var form = new InteractiveForm();
            form.Show();
        }

        /// <summary>
        /// Static method to create and show the form modally
        /// </summary>
        public static void ShowModalForm()
        {
            var form = new InteractiveForm();
            // Use Show() for now - ShowModal may not be available in this Eto version
            form.Show();
        }
    }
}