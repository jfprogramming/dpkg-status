#!/bin/bash

# Set target environment variables
export QML2_IMPORT_PATH="/usr/share/appdpkg-status/qml/"
export LD_LIBRARY_PATH="/usr/lib/appdpkg-status/:$LD_LIBRARY_PATH"
export QT_PLUGIN_PATH="/usr/lib/appdpkg-status/:$QT_PLUGIN_PATH"
export QT_QUICK_BACKEND="software"

# Print environment variables for verification
echo "Environment variables set for this session:"
echo "PATH=$PATH"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
echo "QML2_IMPORT_PATH=$QML2_IMPORT_PATH"
echo "QT_PLUGIN_PATH=$QT_PLUGIN_PATH"

# Optional: Add the environment variables to ~/.bashrc for persistence
read -p "Do you want to make these changes permanent? (y/n): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    if [[ -w ~/.bashrc ]]; then
        echo "export LD_LIBRARY_PATH=\"/usr/lib/appdpkg-status:\$LD_LIBRARY_PATH\"" >> ~/.bashrc
        echo "export QML2_IMPORT_PATH=\"/usr/share/appdpkg-status/qml:\$QML2_IMPORT_PATH\"" >> ~/.bashrc
        echo "export QT_PLUGIN_PATH=\"/usr/lib/appdpkg-status:\$QT_PLUGIN_PATH\"" >> ~/.bashrc
        echo "export QT_QUICK_BACKEND=\"software\"" >> ~/.bashrc
        echo "Environment variables have been added to ~/.bashrc."
        echo "Please restart your terminal or run 'source ~/.bashrc' to apply the changes."
    else
        echo "Error: Unable to write to ~/.bashrc. Please check your permissions."
    fi
else
    echo "Changes are temporary for this session."
fi