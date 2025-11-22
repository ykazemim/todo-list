#!/bin/bash
# Install the ToDo List scheduler as a systemd service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVICE_FILE="$PROJECT_DIR/systemd/todolist-scheduler.service"
SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "Installing ToDo List scheduler service..."

# Create user systemd directory if it doesn't exist
mkdir -p "$SYSTEMD_DIR"

# Copy service file and update paths
sed "s|%i|$USER|g" "$SERVICE_FILE" > "$SYSTEMD_DIR/todolist-scheduler.service"

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
