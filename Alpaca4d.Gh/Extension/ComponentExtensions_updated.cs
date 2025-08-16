using Grasshopper.Kernel;
using Grasshopper.Kernel.Special;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace Alpaca4d.Gh
{
    /// <summary>
    /// Utility class for updating ValueList components in Grasshopper
    /// </summary>
    public static class ValueListUtils
    {
        /// <summary>
        /// Updates ValueList components connected to a specific input parameter
        /// </summary>
        /// <param name="component">The Grasshopper component</param>
        /// <param name="inputIndex">Index of the input parameter</param>
        /// <param name="names">List of names to populate the ValueList with</param>
        /// <param name="values">Optional list of values corresponding to the names</param>
        /// <param name="listMode">Mode for the ValueList (dropdown, list, etc.)</param>
        public static void UpdateValueLists(
            GH_Component component, 
            int inputIndex, 
            List<string> names, 
            List<int> values = null, 
            GH_ValueListMode listMode = GH_ValueListMode.DropDown)
        {
            // Early return if no names provided
            if (names == null || names.Count == 0)
            {
                return;
            }

            // Get the input parameter
            var inputParam = component.Params.Input[inputIndex];
            if (inputParam == null)
            {
                return;
            }

            // Iterate through all sources connected to this input
            foreach (var source in inputParam.Sources)
            {
                // Check if the source is a ValueList
                if (source is GH_ValueList valueList)
                {
                    UpdateSingleValueList(valueList, names, values, listMode);
                }
            }
        }

        /// <summary>
        /// Updates a single ValueList component with new items
        /// </summary>
        /// <param name="valueList">The ValueList to update</param>
        /// <param name="names">List of names to populate the ValueList with</param>
        /// <param name="values">Optional list of values corresponding to the names</param>
        /// <param name="listMode">Mode for the ValueList</param>
        private static void UpdateSingleValueList(
            GH_ValueList valueList, 
            List<string> names, 
            List<int> values, 
            GH_ValueListMode listMode)
        {
            // Get current item names for comparison
            var currentItemNames = valueList.ListItems.Select(item => item.Name).ToList();
            
            // Check if the lists are already the same
            if (names.SequenceEqual(currentItemNames))
            {
                return; // No update needed
            }

            // Store currently selected items to restore them later
            var selectedItemNames = valueList.SelectedItems.Select(item => item.Name).ToList();

            // Clear existing items
            valueList.ListItems.Clear();

            // Add new items
            if (values == null || values.Count != names.Count)
            {
                // Use names as both display name and value
                foreach (var name in names)
                {
                    var item = new GH_ValueListItem(name, $"\"{name}\"");
                    valueList.ListItems.Add(item);
                }
            }
            else
            {
                // Use provided values
                for (int i = 0; i < names.Count; i++)
                {
                    var item = new GH_ValueListItem(names[i], values[i].ToString());
                    valueList.ListItems.Add(item);
                }
            }

            // Restore previously selected items if they still exist
            foreach (var selectedName in selectedItemNames)
            {
                int index = names.IndexOf(selectedName);
                if (index != -1)
                {
                    valueList.ToggleItem(index);
                }
            }

            // Update the list mode and expire the solution
            valueList.ListMode = listMode;
            valueList.ExpireSolution(true);
        }

        /// <summary>
        /// Updates a ValueList with enum values
        /// </summary>
        /// <typeparam name="T">The enum type</typeparam>
        /// <param name="component">The Grasshopper component</param>
        /// <param name="inputIndex">Index of the input parameter</param>
        /// <param name="listMode">Mode for the ValueList</param>
        public static void UpdateValueListWithEnum<T>(
            GH_Component component, 
            int inputIndex, 
            GH_ValueListMode listMode = GH_ValueListMode.DropDown) where T : Enum
        {
            var enumNames = Enum.GetNames(typeof(T)).ToList();
            var enumValues = Enum.GetValues(typeof(T)).Cast<int>().ToList();
            
            UpdateValueLists(component, inputIndex, enumNames, enumValues, listMode);
        }

        /// <summary>
        /// Gets all ValueList components connected to a specific input
        /// </summary>
        /// <param name="component">The Grasshopper component</param>
        /// <param name="inputIndex">Index of the input parameter</param>
        /// <returns>List of connected ValueList components</returns>
        public static List<GH_ValueList> GetConnectedValueLists(GH_Component component, int inputIndex)
        {
            var valueLists = new List<GH_ValueList>();
            
            if (inputIndex >= 0 && inputIndex < component.Params.Input.Count)
            {
                var inputParam = component.Params.Input[inputIndex];
                foreach (var source in inputParam.Sources)
                {
                    if (source is GH_ValueList valueList)
                    {
                        valueLists.Add(valueList);
                    }
                }
            }
            
            return valueLists;
        }
    }
}