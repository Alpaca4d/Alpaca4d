using System.IO;
using Newtonsoft.Json;

namespace Alpaca4d
{
    public static class AlpacaSettings
    {
        private static readonly string SettingsFilePath =
            System.IO.Path.Combine(Application.GhAlpacaFolder, "settings.json");

        private static string _openSeesPath;
        private static bool _loaded;

        public static string OpenSeesPath
        {
            get
            {
                if (!_loaded)
                    Load();
                return _openSeesPath;
            }
            set
            {
                _openSeesPath = value;
                _loaded = true;
                Save();
            }
        }

        public static void Load()
        {
            _loaded = true;
            try
            {
                if (File.Exists(SettingsFilePath))
                {
                    string json = File.ReadAllText(SettingsFilePath);
                    _openSeesPath = JsonConvert.DeserializeObject<string>(json);
                }
            }
            catch
            {
                // Best-effort load
            }
        }

        public static void Save()
        {
            try
            {
                string json = JsonConvert.SerializeObject(_openSeesPath);
                File.WriteAllText(SettingsFilePath, json);
            }
            catch
            {
                // Best-effort save
            }
        }
    }
}
