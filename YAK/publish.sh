#!/bin/bash

# Simple Alpaca4d Plugin Publishing Script
set -e  # Exit on any error

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YAK_DIR="$PROJECT_ROOT/YAK"
MANIFEST_FILE="$YAK_DIR/manifest.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get current version from manifest
get_current_version() {
    grep "^version:" "$MANIFEST_FILE" | sed 's/version: //'
}

# Update version in manifest
update_version() {
    local new_version="$1"
    print_status "Updating version to $new_version in manifest.yml"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^version: .*/version: $new_version/" "$MANIFEST_FILE"
    else
        sed -i "s/^version: .*/version: $new_version/" "$MANIFEST_FILE"
    fi
    
    print_success "Version updated to $new_version"
}

# Main execution
main() {
    print_status "Starting Alpaca4d plugin publishing process..."
    
    # Get current version
    local current_version=$(get_current_version)
    print_status "Current version: $current_version"
    
    # Ask for new version
    echo -n "Enter new version (or press Enter to keep $current_version): "
    read new_version
    
    if [ -z "$new_version" ]; then
        new_version="$current_version"
    fi
    
    # Check if this is a prerelease version
    if [[ "$new_version" =~ -.*$ ]]; then
        print_status "Detected prerelease version: $new_version"
        echo -n "This is a prerelease. Users will need --prerelease flag to find it. Continue? (Y/n): "
        read prerelease_confirm
        if [[ "$prerelease_confirm" =~ ^[Nn]$ ]]; then
            print_status "Publishing cancelled"
            exit 0
        fi
    fi
    
    # Update version if different
    if [ "$new_version" != "$current_version" ]; then
        update_version "$new_version"
        current_version="$new_version"
    fi
    
    # Step 1: Build with msbuild (macOS)
    print_status "Building project with msbuild..."
    cd "$PROJECT_ROOT"
    msbuild Alpaca4d.Gh/Alpaca4d.Gh.csproj /p:Configuration=Release /p:Platform=AnyCPU
    
    if [ $? -ne 0 ]; then
        print_error "Build failed"
        exit 1
    fi
    print_success "Build completed"
    
    # Step 2: Create version directory and collect files
    print_status "Collecting files for version $current_version..."
    local version_dir="$YAK_DIR/$current_version"
    mkdir -p "$version_dir"
    
    # Find the output directory (should be net48 for SDK-style project)
    local output_dir="$PROJECT_ROOT/Alpaca4d.Gh/bin/Release"
    if [ -d "$output_dir/net48" ]; then
        output_dir="$output_dir/net48"
    fi
    
    # Copy all files
    cp "$output_dir/"*.dll "$version_dir/"
    cp "$output_dir/Alpaca4d.Gh.gha" "$version_dir/"
    cp -r "$output_dir/OpenSees-Solvers" "$version_dir/"
    cp "$output_dir/data.bin" "$version_dir/"
    cp -r "$output_dir/UserObject" "$version_dir/"
    
    # Copy manifest and icon for yak build
    cp "$YAK_DIR/manifest.yml" "$version_dir/"
    cp "$YAK_DIR/icon.png" "$version_dir/"
    
    print_success "Files collected in $version_dir"
    
    # Step 3: Create yak file
    print_status "Creating yak package..."
    cd "$version_dir"
    
    # Build the package (will auto-detect rhino version)
    yak build --platform any
    
    # Find the generated .yak file and rename it to any-any
    local original_yak=$(ls *.yak 2>/dev/null | head -1)
    if [ -n "$original_yak" ]; then
        # Extract the base name and replace the rhino version with 'any'
        local new_name=$(echo "$original_yak" | sed 's/-rh[0-9_]*-/-any-/')
        if [ "$original_yak" != "$new_name" ]; then
            mv "$original_yak" "$new_name"
            print_status "Renamed $original_yak to $new_name"
        fi
    fi
    
    # Clean up any extra .yak files (in case folder already existed)
    local yak_count=$(ls *.yak 2>/dev/null | wc -l)
    if [ "$yak_count" -gt 1 ]; then
        print_status "Multiple .yak files found, keeping only the any-any version"
        ls *.yak | grep -v "any-any" | xargs rm -f
    fi
    
    # Clean up temporary files but keep the .yak
    rm manifest.yml icon.png
    
    print_success "Package created: $(ls *.yak)"
    print_success "Publishing process completed!"
    
    # Ask if user wants to push
    echo -n "Do you want to push to Package Manager? (Y/n): "
    read push_answer
    
    if [[ "$push_answer" =~ ^[Yy]$ ]]; then
        print_status "Pushing package..."
        local yak_file=$(ls *.yak 2>/dev/null | head -1)
        if [ -n "$yak_file" ]; then
            yak push "./$yak_file"
            if [ $? -eq 0 ]; then
                print_success "Package pushed successfully!"
            else
                print_error "Failed to push package"
            fi
        else
            print_error "No .yak file found to push"
        fi
    else
        print_status "Package ready in $version_dir"
    fi
}

# Run main function
main "$@"