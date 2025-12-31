#!/bin/bash
# Deploy script for NFC Spotify Record Player
# Usage: ./deploy.sh

PI_HOST="10.0.0.114"
PI_USER="pi"
PI_DIR="/home/pi/raspberryPiRecordPlayer"

echo "=== NFC Spotify Record Player Deployment ==="

# 1. Sync files to Pi
echo "[1/5] Syncing files to Raspberry Pi..."
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude 'logs' \
    ./ ${PI_USER}@${PI_HOST}:${PI_DIR}/

# 2. Create logs directory
echo "[2/5] Creating logs directory..."
ssh ${PI_USER}@${PI_HOST} "mkdir -p ${PI_DIR}/logs"

# 3. Install Node dependencies on Pi
echo "[3/5] Installing Node.js dependencies..."
ssh ${PI_USER}@${PI_HOST} "cd ${PI_DIR} && npm install"

# 4. Install and enable systemd service
echo "[4/5] Setting up systemd service..."
ssh ${PI_USER}@${PI_HOST} "sudo cp ${PI_DIR}/nfc-spotify.service /etc/systemd/system/ && \
    sudo systemctl daemon-reload && \
    sudo systemctl enable nfc-spotify.service"

# 5. Restart the service
echo "[5/5] Restarting service..."
ssh ${PI_USER}@${PI_HOST} "sudo systemctl restart nfc-spotify.service"

echo ""
echo "=== Deployment complete! ==="
echo ""
echo "Useful commands:"
echo "  Check status:  ssh ${PI_USER}@${PI_HOST} 'sudo systemctl status nfc-spotify'"
echo "  View logs:     ssh ${PI_USER}@${PI_HOST} 'tail -f ${PI_DIR}/logs/player.log'"
echo "  Restart:       ssh ${PI_USER}@${PI_HOST} 'sudo systemctl restart nfc-spotify'"
