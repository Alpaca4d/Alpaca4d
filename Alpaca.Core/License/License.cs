using System.Collections.Generic;
using Newtonsoft.Json;
using System.IO;
using System;
using System.Linq;
using System.Net.NetworkInformation;
using System.Reflection;


namespace Alpaca4d.License
{
    public static class License
    {
        public static string assemblyLocation = Assembly.GetExecutingAssembly().Location;
        public static string GhAlpacaFolder = System.IO.Path.GetDirectoryName(assemblyLocation);
        public static string licenseLocation = System.IO.Path.Combine(GhAlpacaFolder, @"data.bin");
        public static bool IsValid
        {
            get
            {
                var addresses = GetMacAddress();
                var users = License.DeserializeBinary(licenseLocation);

                // check data.bin
                foreach (var user in users)
                {
                    if(user.user_name == "FreeVersion")
                    {
                        if(DateTime.Now < user.expiring_date)
                            return true;
                    }

                    foreach(var macAdress in addresses)
                    {
                        if((macAdress == user.mac_address) && (DateTime.Now < user.expiring_date))
                                return true;
                    }
                }
                return false;
            }
        }

        public static List<string> GetMacAddress()
        {
            var macAddress = NetworkInterface.GetAllNetworkInterfaces().Select(x => x.GetPhysicalAddress().ToString()).ToList();
            return macAddress;
        }


        // method for Alpaca4d to read back the results
        public static List<User> DeserializeBinary(string filePath)
        {
            byte[] binaryData = File.ReadAllBytes(filePath);
            var deserializedObject = MessagePack.MessagePackSerializer.Typeless.Deserialize(binaryData);
            var myobject = (List<User>)deserializedObject;
            return myobject;
        }

        public static byte[] SerializeJsonToBinary(string filePath)
        {
            byte[] binaryData;

            string jsonData = System.IO.File.ReadAllText(filePath);
            var myObject = Newtonsoft.Json.JsonConvert.DeserializeObject<List<User>>(jsonData);

            binaryData = MessagePack.MessagePackSerializer.Typeless.Serialize(myObject);
            return binaryData;
        }

        public static void SerializeBinaryToFile(string filePath, byte[] binaryData)
        {
            File.WriteAllBytes(filePath, binaryData);
        }

        public static List<User> DeserialiseJSON(string filePath)
        {
            string jsonData = System.IO.File.ReadAllText(filePath);
            var users = JsonConvert.DeserializeObject<List<User>>(jsonData);

            return users;
        }
    }

    public class User
    {
        public string user_name { get; set; }
        public string mac_address { get; set; }
        public System.DateTime expiring_date { get; set; }
    }

}

