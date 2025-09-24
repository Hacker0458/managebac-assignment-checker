#!/bin/bash
# Test script to verify install.sh fix

echo "🧪 Testing install.sh fix..."

# Test 1: Check if requirements.txt exists on GitHub
echo "📋 Testing requirements.txt availability..."
if curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt" | head -1 | grep -q "ManageBac"; then
    echo "✅ requirements.txt is available on GitHub"
else
    echo "❌ requirements.txt is not available on GitHub"
fi

# Test 2: Check if requirements-core.txt exists on GitHub
echo "📋 Testing requirements-core.txt availability..."
if curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements-core.txt" | head -1 | grep -q "404"; then
    echo "✅ requirements-core.txt correctly returns 404 (doesn't exist)"
else
    echo "❌ requirements-core.txt exists (unexpected)"
fi

# Test 3: Simulate the download process
echo "📦 Testing download process..."
mkdir -p /tmp/test_install
cd /tmp/test_install

echo "Downloading requirements.txt..."
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt" -o requirements.txt

if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
    echo "✅ requirements.txt downloaded successfully"
    echo "📄 First few lines:"
    head -5 requirements.txt
else
    echo "❌ requirements.txt download failed"
fi

# Cleanup
cd ~
rm -rf /tmp/test_install

echo "🎉 Test completed!"

