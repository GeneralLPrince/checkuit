 #!/bin/bash

# Function to install Python (for Linux/macOS)
install_python() {
    if ! command -v python3 &> /dev/null
    then
        echo "Python3 not found. Installing..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get install python3 -y
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python3
        else
            echo "Unsupported OS. Please install Python manually."
            exit 1
        fi
    else
        echo "Python3 is already installed."
    fi
}

# Install Python if necessary
install_python

# Clone the GitHub repository to the user's Documents folder
TARGET_DIR="$HOME/Documents/checkuit"

# Check if the directory already exists
if [ -d "$TARGET_DIR" ]; then
    echo "checkuit is already installed in $TARGET_DIR"
else
    echo "Cloning checkuit from GitHub..."
    git clone https://github.com/yourusername/checkuit.git "$TARGET_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to clone checkuit repository."
        exit 1
    fi
    echo "checkuit has been successfully cloned to $TARGET_DIR"
fi

# Set up alias
ALIAS="alias checkuit='python3 $TARGET_DIR/checkuit.py'"

# Determine which profile to use based on the shell
if [ -n "$BASH_VERSION" ]; then
    PROFILE=~/.bashrc
elif [ -n "$ZSH_VERSION" ]; then
    PROFILE=~/.zshrc
else
    echo "Unsupported shell. Please manually add the alias."
    exit 1
fi

# Check if alias is already in the profile
if grep -Fxq "$ALIAS" "$PROFILE"
then
    echo "Alias already exists in $PROFILE"
else
    # Add the alias to the profile
    echo "$ALIAS" >> "$PROFILE"
    echo "Alias added to $PROFILE. Sourcing the profile to apply changes..."
    source "$PROFILE"
fi

echo "Installation complete. Run 'checkuit <your_assignment_file>' to test your code."
