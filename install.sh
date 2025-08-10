# Check that node and npm are installed, if they are not, try to install it using nvm

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
	echo "Node.js or npm not found. Installing via nvm..."
	if ! command -v nvm >/dev/null 2>&1; then
		# Install nvm
		curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
		export NVM_DIR="$HOME/.nvm"
		[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
	else
		export NVM_DIR="$HOME/.nvm"
		[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
	fi
	nvm install --lts
fi

# Check that pnpm is installed
if ! command -v pnpm >/dev/null 2>&1; then
	echo "pnpm not found. Installing..."
	npm install -g pnpm
fi

# Install project dependencies
cd frontend
pnpm install

# Check that python3 and pip are installed
if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 not found. Please install it."
	exit
fi

if ! command -v pip >/dev/null 2>&1; then
	echo "pip not found. Please install it."
	exit
fi

# Go in the backend folder, create a virtual environment and install dependencies
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Installation complete."