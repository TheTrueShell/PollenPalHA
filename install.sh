#!/bin/bash

# PollenPal Home Assistant Integration Installer
# This script helps install the PollenPal integration to your Home Assistant instance

set -e

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Default Home Assistant config directory
DEFAULT_HA_CONFIG="/config"

echo -e "${BLUE}🌾 PollenPal Home Assistant Integration Installer${NC}"
echo "=================================================="

# Function to print coloured messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root (not recommended for HA)
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. Make sure this is correct for your Home Assistant setup."
fi

# Get Home Assistant config directory
echo
print_info "Please enter your Home Assistant configuration directory path:"
print_info "Common paths:"
print_info "  - Docker/Supervised: /config"
print_info "  - Core installation: ~/.homeassistant"
print_info "  - HAOS: /homeassistant"
echo
read -p "Enter path (default: $DEFAULT_HA_CONFIG): " HA_CONFIG_DIR
HA_CONFIG_DIR=${HA_CONFIG_DIR:-$DEFAULT_HA_CONFIG}

# Validate directory exists
if [ ! -d "$HA_CONFIG_DIR" ]; then
    print_error "Directory $HA_CONFIG_DIR does not exist!"
    print_info "Please check your Home Assistant configuration directory path."
    exit 1
fi

# Check if configuration.yaml exists (basic validation)
if [ ! -f "$HA_CONFIG_DIR/configuration.yaml" ]; then
    print_warning "configuration.yaml not found in $HA_CONFIG_DIR"
    print_warning "Are you sure this is your Home Assistant config directory?"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled."
        exit 1
    fi
fi

# Create custom_components directory if it doesn't exist
CUSTOM_COMPONENTS_DIR="$HA_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    print_info "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
    print_success "Created $CUSTOM_COMPONENTS_DIR"
fi

# Create pollenpal directory
POLLENPAL_DIR="$CUSTOM_COMPONENTS_DIR/pollenpal"
if [ -d "$POLLENPAL_DIR" ]; then
    print_warning "PollenPal integration already exists in $POLLENPAL_DIR"
    read -p "Overwrite existing installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled."
        exit 1
    fi
    print_info "Removing existing installation..."
    rm -rf "$POLLENPAL_DIR"
fi

print_info "Creating PollenPal integration directory..."
mkdir -p "$POLLENPAL_DIR"

# Copy integration files
print_info "Installing PollenPal integration files..."

# Check if we're in the source directory
if [ ! -f "custom_components/pollenpal/__init__.py" ]; then
    print_error "PollenPal source files not found!"
    print_info "Please run this script from the PollenPal integration directory."
    exit 1
fi

# Copy all integration files
cp -r custom_components/pollenpal/* "$POLLENPAL_DIR/"

print_success "PollenPal integration files installed successfully!"

# Set appropriate permissions
print_info "Setting file permissions..."
chmod -R 644 "$POLLENPAL_DIR"
find "$POLLENPAL_DIR" -type d -exec chmod 755 {} \;

print_success "File permissions set correctly."

# Installation complete
echo
print_success "🎉 PollenPal integration installed successfully!"
echo
print_info "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services → Add Integration"
echo "3. Search for 'PollenPal' and configure it"
echo "4. Enter your PollenPal API URL and location"
echo
print_info "For configuration examples, check the examples/ directory:"
echo "  - examples/configuration.yaml - Home Assistant config examples"
echo "  - examples/lovelace-dashboard.yaml - Dashboard examples"
echo
print_info "For troubleshooting, enable debug logging:"
echo "  logger:"
echo "    logs:"
echo "      custom_components.pollenpal: debug"
echo
print_warning "Remember to have your PollenPal API running and accessible!"
print_info "Visit https://github.com/TheTrueShell/PollenPal for API setup instructions."
echo
print_success "Installation complete! 🌾" 