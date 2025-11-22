#!/bin/bash
# Install the ToDo List scheduler as a systemd service

set -e

# Check if running with sudo
if [ "$EUID" -eq 0 ]; then
    echo "❌ Error: Do not run this script with sudo!"
    echo ""
    echo "Systemd user services must be installed by the regular user."
    echo "Please run without sudo:"
    echo "  ./scripts/install-scheduler-service.sh"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVICE_FILE="$PROJECT_DIR/systemd/todolist-scheduler.service"
SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "Installing ToDo List scheduler service..."

# Check if systemd user services are available
if ! systemctl --user list-units &>/dev/null; then
    echo "⚠️  Warning: Systemd user services may not be available."
    echo "   Make sure you're logged into a graphical session or have enabled lingering."
    echo ""
    echo "To enable lingering (allows user services without active session):"
    echo "  sudo loginctl enable-linger $USER"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create user systemd directory if it doesn't exist
mkdir -p "$SYSTEMD_DIR"

# Copy service file and update paths with actual user and project directory
USER_HOME=$(eval echo ~$USER)
sed -e "s|%i|$USER|g" -e "s|/home/%i|$USER_HOME|g" "$SERVICE_FILE" > "$SYSTEMD_DIR/todolist-scheduler.service"

# Make startup script executable
chmod +x "$PROJECT_DIR/scripts/start-scheduler.sh"

# Reload systemd
systemctl --user daemon-reload

echo "✅ Service installed successfully!"
echo ""
echo "To start the service:"
echo "  systemctl --user start todolist-scheduler"
echo ""
echo "To enable auto-start on boot:"
echo "  systemctl --user enable todolist-scheduler"
echo ""
echo "To check status:"
echo "  systemctl --user status todolist-scheduler"
echo ""
echo "To view logs:"
echo "  journalctl --user -u todolist-scheduler -f"
