import pyperclip

def to_circled_number(num):
    circled_numbers = ['⓪', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']
    return ''.join(circled_numbers[int(digit)] for digit in str(num) if digit.isdigit())

# 从剪贴板读取内容
clipboard_content = pyperclip.paste()

# 将阿拉伯数字转换为带圈数字
circled_number = to_circled_number(clipboard_content)

# 将结果复制回剪贴板
pyperclip.copy(circled_number)

print(f"转换后的内容已复制到剪贴板: {circled_number}")