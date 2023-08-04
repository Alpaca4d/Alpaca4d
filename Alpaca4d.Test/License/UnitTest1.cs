using LicenseObfuscation;
using System.Linq;
using System.Net.NetworkInformation;
using Alpaca4d.License;

namespace LicenseObfuscation.Test;

public class UnitTest1
{
    [TestMethod]
    public void Test1()
    {
        var users = License.DeserialiseJSON(@"data.json");
        Assert.IsNotNull(users);
        Assert.IsTrue(users.Count == 3);
        Assert.IsTrue(users[0].user_name == "marcopellegrino");
        Assert.IsTrue(users[0].mac_address == "A6BF4E24B94C");
        Assert.IsTrue(users[0].expiring_date == DateTime.Parse("2023-09-01"));

        Assert.IsTrue(users[1].user_name == "saraandreussi");
        Assert.IsTrue(users[1].mac_address == "5CE91E989E12");
        Assert.IsTrue(users[1].expiring_date == DateTime.Parse("2024-01-01"));
    }

    [TestMethod]

    public void Test2()
    {
        var jsonFilePath = "data.json";
        var binaryFilePath = "data.bin";

        var binary = License.SerializeJsonToBinary(jsonFilePath);
        License.SerializeBinaryToFile(binaryFilePath, binary);
        var usersObj = License.DeserializeBinary(binaryFilePath);

        var users = (List<User>)usersObj;
        Assert.IsNotNull(users);
        Assert.IsTrue(users.Count == 3);
        Assert.IsTrue(users[0].user_name == "marcopellegrino");
        Assert.IsTrue(users[0].mac_address == "A6BF4E24B94C");
        Assert.IsTrue(users[0].expiring_date == DateTime.Parse("2023-09-01"));

        Assert.IsTrue(users[1].user_name == "saraandreussi");
        Assert.IsTrue(users[1].mac_address == "5CE91E989E12");
        Assert.IsTrue(users[1].expiring_date == DateTime.Parse("2024-01-01"));
    }

    [TestMethod]
    public void Test3()
    {
        var networkInterfaces = NetworkInterface.GetAllNetworkInterfaces();

        var macAdresses = networkInterfaces.Select(x => x.GetPhysicalAddress().ToString());
    }

    [TestMethod]
    public void Test4()
    {
        bool res = false;

        var macAddress = NetworkInterface.GetAllNetworkInterfaces().Select(x => x.GetPhysicalAddress().ToString()).ToList();
        var users = License.DeserializeBinary("data.bin");

        foreach (var user in users)
        {
            if (macAddress.Any(x => x == user.mac_address))
            {
                res = true;
                break;
            }
        }

        Assert.IsTrue(res);
    }


    [TestMethod]
    public void Test5()
    {
        bool res = false;

        var macAddress = new List<string> { "XXZZAASSDDQQ" };
        var users = License.DeserializeBinary("data.bin");

        foreach (var user in users)
        {
            if (macAddress.Any(x => x == user.mac_address))
            {
                res = true;
                break;
            }
        }

        Assert.IsFalse(res);
    }

}