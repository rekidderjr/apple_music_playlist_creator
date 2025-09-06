#!/bin/bash

# Project Setup Script
# Initializes a new project with all compliance and security features
# Author: rekidderjr

set -e

echo "Setting up your new secure Python project..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project details from user
read -p "Enter your project name (e.g., my-awesome-project): " PROJECT_NAME
read -p "Enter your name: " AUTHOR_NAME
read -p "Enter your email: " AUTHOR_EMAIL
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Validate inputs
if [ -z "$PROJECT_NAME" ] || [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ] || [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}All fields are required!${NC}"
    exit 1
fi

# Convert project name to valid Python package name
PACKAGE_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g')

echo -e "\n${BLUE}📝 Project Configuration:${NC}"
echo "Project Name: $PROJECT_NAME"
echo "Package Name: $PACKAGE_NAME"
echo "Author: $AUTHOR_NAME"
echo "Email: $AUTHOR_EMAIL"
echo "GitHub: $GITHUB_USERNAME"

read -p "Continue with this configuration? (y/N): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

echo -e "\n${BLUE}🔧 Customizing project files...${NC}"

# Update package directory name
if [ -d "src/your_package" ]; then
    mv "src/your_package" "src/$PACKAGE_NAME"
fi

# Update pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i.bak "s/your-project-name/$PROJECT_NAME/g" pyproject.toml
    sed -i.bak "s/Your Name/$AUTHOR_NAME/g" pyproject.toml
    sed -i.bak "s/your.email@example.com/$AUTHOR_EMAIL/g" pyproject.toml
    sed -i.bak "s/yourusername/$GITHUB_USERNAME/g" pyproject.toml
    rm pyproject.toml.bak
fi

# Update setup.cfg
if [ -f "setup.cfg" ]; then
    sed -i.bak "s/your-project-name/$PROJECT_NAME/g" setup.cfg
    sed -i.bak "s/Your Name/$AUTHOR_NAME/g" setup.cfg
    sed -i.bak "s/your.email@example.com/$AUTHOR_EMAIL/g" setup.cfg
    rm setup.cfg.bak
fi

# Update README.md
if [ -f "README.md" ]; then
    sed -i.bak "s/Project Name/$PROJECT_NAME/g" README.md
    sed -i.bak "s/yourusername/$GITHUB_USERNAME/g" README.md
    sed -i.bak "s/your-project-name/$PROJECT_NAME/g" README.md
    sed -i.bak "s/your_package/$PACKAGE_NAME/g" README.md
    rm README.md.bak
fi

# Update LICENSE
if [ -f "LICENSE" ]; then
    CURRENT_YEAR=$(date +%Y)
    sed -i.bak "s/2025/$CURRENT_YEAR/g" LICENSE
    sed -i.bak "s/Your Name/$AUTHOR_NAME/g" LICENSE
    rm LICENSE.bak
fi

# Update package __init__.py
if [ -f "src/$PACKAGE_NAME/__init__.py" ]; then
    sed -i.bak "s/Your Package/$PROJECT_NAME/g" "src/$PACKAGE_NAME/__init__.py"
    sed -i.bak "s/Your Name/$AUTHOR_NAME/g" "src/$PACKAGE_NAME/__init__.py"
    sed -i.bak "s/your.email@example.com/$AUTHOR_EMAIL/g" "src/$PACKAGE_NAME/__init__.py"
    rm "src/$PACKAGE_NAME/__init__.py.bak"
fi

# Update test imports
if [ -f "tests/test_main.py" ]; then
    sed -i.bak "s/your_package/$PACKAGE_NAME/g" tests/test_main.py
    rm tests/test_main.py.bak
fi

echo -e "${GREEN}Project files customized successfully!${NC}"

# Check if Python 3.8+ is available
echo -e "\n${BLUE}🐍 Checking Python version...${NC}"
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "Python version: $PYTHON_VERSION"
    
    if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
        echo -e "${GREEN}SUCCESS: Python 3.8+ detected${NC}"
    else
        echo -e "${RED}FAILED: Python 3.8+ required${NC}"
        exit 1
    fi
else
    echo -e "${RED}FAILED: Python 3 not found${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${BLUE}🔧 Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install development dependencies
echo -e "${BLUE}📦 Installing development dependencies...${NC}"
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo -e "${BLUE}🪝 Setting up pre-commit hooks...${NC}"
pre-commit install

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo -e "\n${BLUE}📚 Initializing git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: Secure Python project template

- Complete CI/CD workflows for security and quality
- Comprehensive testing setup
- Pre-commit hooks configured
- Customer compliance checks included"
    
    echo -e "${GREEN}SUCCESS: Git repository initialized${NC}"
else
    echo -e "${YELLOW}⚠️  Git repository already exists${NC}"
fi

# Run compliance check
echo -e "\n${BLUE}CHECKING: Running compliance check...${NC}"
if ./customer-compliance-check.sh; then
    echo -e "${GREEN}SUCCESS: All compliance checks passed!${NC}"
else
    echo -e "${YELLOW}⚠️  Some compliance checks failed, but project is ready for development${NC}"
fi

# Final instructions
echo -e "\n${GREEN}🎉 Project setup complete!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start developing in src/$PACKAGE_NAME/"
echo "3. Write tests in tests/"
echo "4. Run tests: pytest"
echo "5. Check code quality: ./customer-compliance-check.sh"
echo "6. Create GitHub repository and push your code"

echo -e "\n${BLUE}📚 Useful commands:${NC}"
echo "• Format code: black . && isort ."
echo "• Run tests: pytest --cov=src"
echo "• Security scan: bandit -r src/"
echo "• Type check: mypy src/"
echo "• Full compliance: ./customer-compliance-check.sh"

echo -e "\n${GREEN}Happy coding! READY!${NC}"
