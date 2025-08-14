using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using Eto.Forms;
using Eto.Drawing;
using Alpaca4d.License;

namespace Alpaca4d.UI
{
    public class LicenseManagementForm : Form
    {
        private ListBox licenseListBox;
        private Label statusLabel;
        private Button addLicenseButton;
        private Button removeLicenseButton;
        
        private string licenseFilePath;
        private List<User> currentLicenses;

        public LicenseManagementForm()
        {
            InitializeComponent();
            LoadLicenses();
        }

        private void InitializeComponent()
        {
            // Form properties
            Title = "Alpaca4d - License Management";
            Maximizable = false;
            Minimizable = true;
            Resizable = false;
            Topmost = true;
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

            // Initialize license file path
            string assemblyLocation = Assembly.GetExecutingAssembly().Location;
            string alpacaFolder = Path.GetDirectoryName(assemblyLocation);
            licenseFilePath = Path.Combine(alpacaFolder, "data.bin");

            // Create main layout
            Content = CreateMainLayout();
        }

        private Control CreateMainLayout()
        {
            var layout = new TableLayout
            {
                Spacing = new Size(10, 10)
            };

            // Header section
            layout.Rows.Add(CreateHeaderSection());

            // License list section
            layout.Rows.Add(CreateLicenseListSection());

            // Status section
            layout.Rows.Add(CreateStatusSection());

            // Button section
            layout.Rows.Add(CreateButtonSection());

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

            // Title
            var titleLabel = new Label
            {
                Text = "License Management",
                Font = SystemFonts.Bold(16),
                TextAlignment = TextAlignment.Center,
                TextColor = Eto.Drawing.Colors.DarkBlue
            };
            headerLayout.Items.Add(titleLabel);

            // Subtitle
            var subtitleLabel = new Label
            {
                Text = "Manage your Alpaca4d licenses",
                Font = new Font(SystemFont.Default, 10),
                TextAlignment = TextAlignment.Center,
                TextColor = Eto.Drawing.Colors.Gray
            };
            headerLayout.Items.Add(subtitleLabel);

            return headerLayout;
        }

        private Control CreateLicenseListSection()
        {
            var listLayout = new StackLayout
            {
                Orientation = Orientation.Vertical,
                Spacing = 10
            };

            // List label
            var listLabel = new Label
            {
                Text = "Current Licenses:",
                Font = SystemFonts.Bold(12)
            };
            listLayout.Items.Add(listLabel);

            // License list box
            licenseListBox = new ListBox
            {
                Size = new Size(400, 150)
            };
            licenseListBox.SelectedIndexChanged += OnLicenseSelectionChanged;
            listLayout.Items.Add(licenseListBox);

            return listLayout;
        }

        private Control CreateStatusSection()
        {
            var statusLayout = new StackLayout
            {
                Orientation = Orientation.Vertical,
                Spacing = 5
            };

            // Status label
            statusLabel = new Label
            {
                Text = "Ready",
                Font = new Font(SystemFont.Default, 10),
                TextColor = Eto.Drawing.Colors.DarkGreen
            };
            statusLayout.Items.Add(statusLabel);

            // License file path info
            var pathLabel = new Label
            {
                Text = $"License file: {licenseFilePath}",
                Font = new Font(SystemFont.Default, 8),
                TextColor = Eto.Drawing.Colors.Gray
            };
            statusLayout.Items.Add(pathLabel);

            return statusLayout;
        }

        private Control CreateButtonSection()
        {
            var buttonLayout = new TableLayout
            {
                Spacing = new Size(10, 10)
            };

            // Single row with Add and Remove buttons
            var row1 = new TableRow();
            row1.Cells.Add(CreateAddLicenseButton());
            row1.Cells.Add(CreateRemoveLicenseButton());
            buttonLayout.Rows.Add(row1);

            return buttonLayout;
        }

        private Button CreateAddLicenseButton()
        {
            addLicenseButton = new Button
            {
                Text = "➕ Add License",
                Size = new Size(140, 35),
                BackgroundColor = Eto.Drawing.Colors.LightGreen
            };
            
            addLicenseButton.Click += OnAddLicenseClicked;
            return addLicenseButton;
        }

        private Button CreateRemoveLicenseButton()
        {
            removeLicenseButton = new Button
            {
                Text = "➖ Remove License",
                Size = new Size(140, 35),
                BackgroundColor = Eto.Drawing.Colors.LightCoral
            };
            
            removeLicenseButton.Click += OnRemoveLicenseClicked;
            removeLicenseButton.Enabled = false;
            return removeLicenseButton;
        }

        private void LoadLicenses()
        {
            try
            {
                licenseListBox.Items.Clear();
                currentLicenses = new List<User>();

                if (File.Exists(licenseFilePath))
                {
                    currentLicenses = Alpaca4d.License.License.DeserializeBinary(licenseFilePath);
                    
                    foreach (var license in currentLicenses)
                    {
                        string displayText = $"{license.user_name} - Expires: {license.expiring_date:yyyy-MM-dd}";
                        if (license.expiring_date < DateTime.Now)
                        {
                            displayText += " (EXPIRED)";
                        }
                        licenseListBox.Items.Add(displayText);
                    }

                    UpdateStatus($"Loaded {currentLicenses.Count} license(s)", Eto.Drawing.Colors.DarkGreen);
                }
                else
                {
                    UpdateStatus("No license file found", Eto.Drawing.Colors.Orange);
                }
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error loading licenses: {ex.Message}", Eto.Drawing.Colors.Red);
            }
        }

        private void OnLicenseSelectionChanged(object sender, EventArgs e)
        {
            bool hasSelection = licenseListBox.SelectedIndex >= 0;
            removeLicenseButton.Enabled = hasSelection;
        }

        private void OnAddLicenseClicked(object sender, EventArgs e)
        {
            try
            {
                var openFileDialog = new OpenFileDialog();
                openFileDialog.Title = "Select License File";
                openFileDialog.Filters.Add(new FileFilter("License files", "*.bin"));
                openFileDialog.Filters.Add(new FileFilter("All files", "*.*"));

                if (openFileDialog.ShowDialog(this) == DialogResult.Ok)
                {
                    string selectedFilePath = openFileDialog.FileName;
                    string targetDirectory = Path.GetDirectoryName(licenseFilePath);

                    // Ensure the target directory exists
                    if (!Directory.Exists(targetDirectory))
                    {
                        Directory.CreateDirectory(targetDirectory);
                    }

                    // Copy the file to the target location
                    File.Copy(selectedFilePath, licenseFilePath, true);

                    // Verify the license is valid
                    if (Alpaca4d.License.License.IsValid)
                    {
                        UpdateStatus("License added successfully!", Eto.Drawing.Colors.DarkGreen);
                        LoadLicenses(); // Refresh the list
                    }
                    else
                    {
                        UpdateStatus("License file added but appears to be invalid or expired", Eto.Drawing.Colors.Orange);
                        LoadLicenses(); // Refresh the list anyway
                    }
                }
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error adding license: {ex.Message}", Eto.Drawing.Colors.Red);
            }
        }

        private void OnRemoveLicenseClicked(object sender, EventArgs e)
        {
            if (licenseListBox.SelectedIndex < 0) return;

            try
            {
                var result = MessageBox.Show(
                    "Are you sure you want to remove the selected license?",
                    "Confirm License Removal",
                    MessageBoxType.Question);

                if (result == DialogResult.Yes)
                {
                    // Remove the license file
                    if (File.Exists(licenseFilePath))
                    {
                        File.Delete(licenseFilePath);
                        UpdateStatus("License removed successfully", Eto.Drawing.Colors.DarkGreen);
                        LoadLicenses(); // Refresh the list
                    }
                }
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error removing license: {ex.Message}", Eto.Drawing.Colors.Red);
            }
        }



        private void UpdateStatus(string message, Color color)
        {
            statusLabel.Text = message;
            statusLabel.TextColor = color;
        }

        /// <summary>
        /// Static method to create and show the license management form
        /// </summary>
        public static void ShowForm()
        {
            var form = new LicenseManagementForm();
            form.Show();
        }
    }
}