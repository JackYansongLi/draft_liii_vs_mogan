import sys
import os
import subprocess
import tempfile
import uuid

# 路径配置
MOGANSTEM_PATH = "/home/lty/mogan/build/linux/x86_64/release/moganstem"
TEXMACS_PATH = "/home/lty/mogan/TeXmacs"

def escape_latex_for_scheme(latex_str):
    """转义LaTeX字符串中的特殊字符"""
    latex = latex_str.strip()

    # 转义反斜杠
    latex = latex.replace('\\', '\\\\')
    # 转义双引号
    latex = latex.replace('"', '\\"')

    # 确保数学模式
    if not latex.startswith('$'):
        latex = '$' + latex
    if not latex.endswith('$'):
        latex = latex + '$'

    return latex

def generate_scheme_script(latex_lines, output_file_path):
    """生成Scheme脚本，将结果写入文件"""
    scheme_lines = [
        ";; 批量LaTeX转换脚本 - 文件输出版本",
        ";; 自动生成 - 请勿手动编辑",
        ""
    ]

    # 打开输出文件
    scheme_lines.append(f'(let ((out-port (open-output-file "{output_file_path}")))')
    scheme_lines.append('  (dynamic-wind')
    scheme_lines.append('    (lambda () #f)')
    scheme_lines.append('    (lambda ()')

    for i, latex in enumerate(latex_lines):
        if not latex.strip():
            # 空行写入空行
            scheme_lines.append('      (display "" out-port)')
            scheme_lines.append('      (newline out-port)')
            continue

        escaped = escape_latex_for_scheme(latex)
        # 执行转换并写入文件
        scheme_lines.append(f'      (write (tree->stree (latex->texmacs (parse-latex "{escaped}"))) out-port)')
        scheme_lines.append('      (newline out-port)')

    # 关闭文件和处理
    scheme_lines.append('      (close-output-port out-port))')
    scheme_lines.append('    (lambda ()')
    scheme_lines.append('      (if (port? out-port)')
    scheme_lines.append('          (close-output-port out-port)')
    scheme_lines.append('          #f))))')
    scheme_lines.append('')

    # 添加成功标记
    scheme_lines.append('(display "转换完成\\n")')

    return '\n'.join(scheme_lines)

def batch_convert(input_file, output_file, timeout=120):
    """批量转换主函数"""
    # 检查路径
    if not os.path.exists(MOGANSTEM_PATH):
        print(f"错误：moganstem未找到：{MOGANSTEM_PATH}")
        return False

    if not os.path.exists(TEXMACS_PATH):
        print(f"错误：TeXmacs路径未找到：{TEXMACS_PATH}")
        return False

    # 读取输入
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_lines = [line.rstrip('\n') for line in f]
    except Exception as e:
        print(f"读取输入文件失败：{e}")
        return False

    total_lines = len(latex_lines)
    non_empty = sum(1 for line in latex_lines if line.strip())
    print(f"读取 {total_lines} 行，其中 {non_empty} 行非空")

    # 创建临时Scheme脚本
    scheme_code = generate_scheme_script(latex_lines, output_file)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.scm', delete=False) as f:
        f.write(scheme_code)
        scheme_file = f.name

    print(f"生成Scheme脚本: {scheme_file}")
    print(f"输出将直接写入: {output_file}")

    try:
        # 设置环境
        env = os.environ.copy()
        env['TEXMACS_PATH'] = TEXMACS_PATH

        # 执行moganstem
        print("执行转换...（可能需要一些时间，取决于表达式数量和复杂度）")
        result = subprocess.run(
            [MOGANSTEM_PATH, '-headless', '-b', scheme_file, '-q'],
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        print(f"执行完成，返回码: {result.returncode}")

        if result.returncode != 0:
            print(f"警告：moganstem返回非零代码: {result.returncode}")
            if result.stderr:
                print(f"stderr前200字符: {result.stderr[:200]}")

        # 检查输出文件
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            print(f"输出文件包含 {len(lines)} 行")

            # 显示示例
            if lines:
                print("\n前3个转换结果:")
                for i, line in enumerate(lines[:3], 1):
                    line = line.rstrip('\n')
                    print(f"{i}. {line[:80]}{'...' if len(line) > 80 else ''}")

            # 验证行数
            if len(lines) != total_lines:
                print(f"警告：输出行数({len(lines)})与输入行数({total_lines})不匹配")
                print("可能是某些转换失败或产生了多行输出")

            return True
        else:
            print(f"错误：输出文件未创建: {output_file}")
            print("可能Scheme执行失败")
            return False

    except subprocess.TimeoutExpired:
        print(f"错误：转换超时（{timeout}秒）")
        print("建议：增加超时时间或减少批量大小")
        return False
    except Exception as e:
        print(f"转换过程中出错：{e}")
        return False
    finally:
        # 清理临时文件
        try:
            os.unlink(scheme_file)
        except:
            pass

def main():
    if len(sys.argv) != 3:
        print("用法：python3 latex_to_scheme_final.py 输入文件.txt 输出文件.scm")
        print("示例：python3 latex_to_scheme_final.py latex.txt results.scm")
        print("\n选项：")
        print("  输入文件：每行一条LaTeX表达式")
        print("  输出文件：每行一个S-expression结果")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"输入文件不存在：{input_file}")
        sys.exit(1)

    print("批量LaTeX到Scheme S-expression转换（文件输出版）")
    print("=" * 60)
    print(f"输入文件: {input_file} ({os.path.getsize(input_file)} 字节)")
    print(f"输出文件: {output_file}")
    print(f"moganstem路径: {MOGANSTEM_PATH}")
    print(f"超时时间: 120秒")
    print("=" * 60)

    if batch_convert(input_file, output_file, timeout=120):
        print("\n✅ 转换成功完成！")
        print(f"结果保存在: {output_file}")
    else:
        print("\n❌ 转换失败")
        sys.exit(1)

if __name__ == '__main__':
    main()