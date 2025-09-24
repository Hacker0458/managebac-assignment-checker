#!/bin/bash
# Test GitHub installation scripts

echo "🧪 Testing GitHub Installation Scripts"
echo "========================================"

# Test 1: Check if requirements.txt is available
echo "📋 Testing requirements.txt availability..."
REQUIREMENTS_CONTENT=$(curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt")
if echo "$REQUIREMENTS_CONTENT" | grep -q "ManageBac"; then
    echo "✅ requirements.txt is available on GitHub"
    echo "📄 First few lines:"
    echo "$REQUIREMENTS_CONTENT" | head -5
else
    echo "❌ requirements.txt is not available or empty"
fi

echo ""

# Test 2: Check if requirements-core.txt exists (should not)
echo "📋 Testing requirements-core.txt availability..."
CORE_REQUIREMENTS=$(curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements-core.txt")
if echo "$CORE_REQUIREMENTS" | grep -q "404"; then
    echo "✅ requirements-core.txt correctly returns 404 (doesn't exist)"
else
    echo "❌ requirements-core.txt exists (unexpected)"
fi

echo ""

# Test 3: Check install.sh content
echo "📋 Testing install.sh content..."
INSTALL_CONTENT=$(curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh")
if echo "$INSTALL_CONTENT" | grep -q "requirements-core.txt"; then
    echo "❌ install.sh still contains requirements-core.txt (needs update)"
else
    echo "✅ install.sh does not contain requirements-core.txt"
fi

echo ""

# Test 4: Check if quick_install.sh exists
echo "📋 Testing quick_install.sh availability..."
QUICK_INSTALL=$(curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh")
if echo "$QUICK_INSTALL" | grep -q "404"; then
    echo "❌ quick_install.sh not available on GitHub"
else
    echo "✅ quick_install.sh is available on GitHub"
fi

echo ""

# Test 5: Check if ultimate_install.sh exists
echo "📋 Testing ultimate_install.sh availability..."
ULTIMATE_INSTALL=$(curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh")
if echo "$ULTIMATE_INSTALL" | grep -q "404"; then
    echo "❌ ultimate_install.sh not available on GitHub"
else
    echo "✅ ultimate_install.sh is available on GitHub"
fi

echo ""
echo "🎯 Test Summary:"
echo "=================="
echo "1. requirements.txt: $(echo "$REQUIREMENTS_CONTENT" | grep -q "ManageBac" && echo "✅ Available" || echo "❌ Not Available")"
echo "2. requirements-core.txt: $(echo "$CORE_REQUIREMENTS" | grep -q "404" && echo "✅ Correctly Missing" || echo "❌ Unexpectedly Available")"
echo "3. install.sh: $(echo "$INSTALL_CONTENT" | grep -q "requirements-core.txt" && echo "❌ Needs Update" || echo "✅ Updated")"
echo "4. quick_install.sh: $(echo "$QUICK_INSTALL" | grep -q "404" && echo "❌ Not Available" || echo "✅ Available")"
echo "5. ultimate_install.sh: $(echo "$ULTIMATE_INSTALL" | grep -q "404" && echo "❌ Not Available" || echo "✅ Available")"

echo ""
echo "🎉 GitHub Installation Test Completed!"

