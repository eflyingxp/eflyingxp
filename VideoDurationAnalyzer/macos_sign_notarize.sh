#!/bin/bash

# macOS应用程序签名和公证脚本

echo "macOS应用程序签名和公证脚本"
echo "----------------------------------------"

# 检查是否提供了开发者ID
if [ "$#" -ne 1 ]; then
    echo "使用方法: $0 '开发者ID'"
    echo "例如: $0 'Developer ID Application: Your Name (ABCDEF1234)'"
    exit 1
fi

DEVELOPER_ID="$1"
APP_PATH="dist/视频时长统计工具.app"
ZIP_PATH="视频时长统计工具.zip"
BUNDLE_ID="com.eflyingxp.videodurationanalyzer"

# 检查应用程序是否存在
if [ ! -d "$APP_PATH" ]; then
    echo "错误: 未找到应用程序 $APP_PATH"
    echo "请先运行打包脚本生成应用程序"
    exit 1
fi

# 签名应用程序
echo "\n正在对应用程序进行签名..."
codesign --force --deep --sign "$DEVELOPER_ID" "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "错误: 签名失败"
    exit 1
fi

echo "签名成功"

# 创建ZIP归档
echo "\n正在创建ZIP归档..."
ditto -c -k --keepParent "$APP_PATH" "$ZIP_PATH"

if [ $? -ne 0 ]; then
    echo "错误: 创建ZIP归档失败"
    exit 1
fi

echo "ZIP归档创建成功: $ZIP_PATH"

# 提交公证
echo "\n准备提交公证..."
echo "请输入您的Apple ID:"
read APPLE_ID

echo "请输入您的应用专用密码(不会显示在屏幕上):"
read -s APP_PASSWORD

echo "\n正在提交公证，这可能需要几分钟时间..."
NOTARIZATION_RESULT=$(xcrun altool --notarize-app \
    --primary-bundle-id "$BUNDLE_ID" \
    --username "$APPLE_ID" \
    --password "$APP_PASSWORD" \
    --file "$ZIP_PATH")

if [ $? -ne 0 ]; then
    echo "错误: 提交公证失败"
    echo "$NOTARIZATION_RESULT"
    exit 1
fi

# 提取请求UUID
REQUEST_UUID=$(echo "$NOTARIZATION_RESULT" | grep 'RequestUUID' | awk '{print $3}')

if [ -z "$REQUEST_UUID" ]; then
    echo "错误: 无法获取请求UUID"
    echo "$NOTARIZATION_RESULT"
    exit 1
fi

echo "公证提交成功，请求UUID: $REQUEST_UUID"

# 等待公证完成
echo "\n正在等待公证完成，这可能需要几分钟时间..."
echo "您可以按Ctrl+C取消等待，稍后使用以下命令检查状态:"
echo "xcrun altool --notarization-info $REQUEST_UUID --username \"$APPLE_ID\" --password \"应用专用密码\""

sleep 10

while true; do
    NOTARIZATION_INFO=$(xcrun altool --notarization-info "$REQUEST_UUID" \
        --username "$APPLE_ID" \
        --password "$APP_PASSWORD")
    
    STATUS=$(echo "$NOTARIZATION_INFO" | grep 'Status:' | awk '{print $2}')
    
    if [ "$STATUS" = "success" ]; then
        echo "\n公证成功!"
        break
    elif [ "$STATUS" = "in" ]; then
        echo "公证仍在进行中，等待30秒..."
        sleep 30
    else
        echo "\n公证失败或状态未知:"
        echo "$NOTARIZATION_INFO"
        exit 1
    fi
done

# 将公证信息附加到应用程序
echo "\n正在将公证信息附加到应用程序..."
xcrun stapler staple "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "错误: 附加公证信息失败"
    exit 1
fi

echo "公证信息附加成功"

# 验证签名和公证
echo "\n正在验证签名和公证..."
spctl --assess --verbose "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "警告: 验证失败，应用程序可能无法正常运行"
else
    echo "验证成功，应用程序已准备好分发"
fi

echo "\n签名和公证过程完成"
echo "您可以将应用程序分发给用户了"