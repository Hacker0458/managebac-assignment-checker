#!/bin/bash

echo "🔧 测试iOS项目构建..."

PROJECT_DIR="/Users/fang/Desktop/💻 开发项目/managebac-assignment-checker"
PROJECT_FILE="$PROJECT_DIR/ManageBacChecker.xcodeproj"

echo "📂 项目路径: $PROJECT_FILE"

# 检查项目文件是否存在
if [ ! -d "$PROJECT_FILE" ]; then
    echo "❌ 项目文件不存在: $PROJECT_FILE"
    exit 1
fi

echo "✅ 项目文件存在"

# 检查可用的模拟器
echo "📱 检查可用的iOS模拟器..."
xcrun simctl list devices available | grep "iPhone"

echo ""
echo "🔨 尝试构建项目..."

# 尝试构建项目
xcodebuild \
    -project "$PROJECT_FILE" \
    -scheme ManageBacChecker \
    -destination "platform=iOS Simulator,name=iPhone 15,OS=latest" \
    -configuration Debug \
    clean build \
    CODE_SIGN_IDENTITY="" \
    CODE_SIGNING_REQUIRED=NO \
    CODE_SIGNING_ALLOWED=NO

BUILD_RESULT=$?

if [ $BUILD_RESULT -eq 0 ]; then
    echo "✅ 构建成功！"
else
    echo "❌ 构建失败，错误代码: $BUILD_RESULT"
    echo ""
    echo "🔍 尝试获取更详细的错误信息..."
    
    # 尝试仅编译而不链接
    xcodebuild \
        -project "$PROJECT_FILE" \
        -scheme ManageBacChecker \
        -destination "platform=iOS Simulator,name=iPhone 15,OS=latest" \
        -configuration Debug \
        -dry-run
fi

echo ""
echo "📋 构建测试完成"

