# Setting up WSL (Windows Subsystem for Linux)

This guide will help you set up WSL with Ubuntu on your Windows system, along with essential development tools.

## Prerequisites
- Windows 10 version 2004 and higher or Windows 11
- Administrator access to your computer

## Step 1: Install WSL and Ubuntu

1. First, check if you have any WSL distributions installed:
   ```powershell
   wsl --list
   ```

2. Install Ubuntu through WSL:
   ```powershell
   wsl --install Ubuntu
   ```

3. **Important**: Restart your computer to complete the installation
   > This step is crucial for WSL to work properly

## Step 2: First-time Ubuntu Setup

1. After reboot, open PowerShell or Command Prompt and start Ubuntu:
   ```powershell
   wsl -d Ubuntu
   ```

2. You'll be prompted to create a new user account:
   - Enter a username (must be lowercase, no spaces)
   - Create a password (8-16 characters recommended)
   > 💡 Note: When typing your password, you won't see any characters on screen - this is normal!

## Step 3: Update Ubuntu System

1. Update the package list and upgrade existing packages:
   ```bash
   sudo apt-get update && sudo apt upgrade -y
   ```

2. Close the terminal completely and open a new one

3. Start Ubuntu again:
   ```powershell
   wsl -d Ubuntu
   ```

## Step 4: Install Development Tools

1. Install essential certificates and Git:
   ```bash
   sudo apt-get install wget ca-certificates git
   ```

2. Install Node Version Manager (nvm):
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
   ```

3. Activate nvm in your current session:
   ```bash
   \. "$HOME/.nvm/nvm.sh"
   ```

4. Install Node.js version 22:
   ```bash
   nvm install 22
   ```

5. Verify Node.js installation:
   ```bash
   node -v    # Should show "v22.15.0"
   nvm current    # Should show "v22.15.0"
   ```

6. Install uv package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

7. **Final Step**: Close and restart your terminal

## Troubleshooting

If you encounter any issues:
- Make sure you've restarted your computer after WSL installation
- Ensure you're running commands with the correct permissions
- Check that your Windows version is compatible with WSL

## Next Steps

You now have a working Ubuntu environment with:
- Git for version control
- Node.js 22 for JavaScript/TypeScript development
- uv package manager for Python development

You're ready to start development! 🚀
