#!/bin/bash

# Path to the binary
binary="build/appdpkg-status"

# Path to the lib directory
lib_dir="build/lib"

# Run ldd on the binary to get the list of linked libraries
echo "Checking missing libraries for $binary..."
ldd_output=$(ldd "$binary")

# Initialize missing libraries array
missing_libraries=()

# Loop through each line of the ldd output
echo "$ldd_output" | while read -r line; do
    # Extract the library path (if it exists)
    lib_path=$(echo "$line" | awk '/=>/ {print $3}')
    
    # If library path is not empty and not found in lib_dir
    if [[ -n "$lib_path" && ! -f "$lib_dir/$(basename "$lib_path")" ]]; then
        echo "Missing: $(basename "$lib_path")"
        missing_libraries+=("$(basename "$lib_path")")
    fi
done

# Print summary of missing libraries
if [[ ${#missing_libraries[@]} -eq 0 ]]; then
    echo "All libraries are present in $lib_dir."
else
    echo "The following libraries are missing in $lib_dir:"
    for lib in "${missing_libraries[@]}"; do
        echo "  - $lib"
    done
fi
