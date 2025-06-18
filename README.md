# NCM to MP3/FLAC Converter | NCMNCM to MP3/FLAC Converter GUI | 网易云音乐转码工具GUI版本 转 MP3/FLAC 转换器

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

This is a GUI version forked from the original MIT-licensed NCM batch converter, now upgraded to support graphical interface operations while maintaining full GPL-3.0-or-later compliance.

### Features

- 🖥️ Dual Mode:
- - Command-line mode: ```python3 ncm_converter.py```
- - GUI mode: ```python3 main.py``` (with progress bar and error handling)
- 🔁 Batch conversion of NCM files to MP3/FLAC
- 📄 Preserves metadata (title, artist, album)
- 🎨 Retains album artwork
- 📊 Real-time conversion progress tracking
- 📋 Detailed logging (saved in .\log\ directory)

### Requirements

- Python 3.14+
- pip (Python package installer)
- tkinter (included with standard Python installations)

The script should install the following dependencies if they are not present:
- pycryptodome
- mutagen

### Installation

1. Clone this repository or download the script:
   ```Bash
   git clone https://github.com/trustedinster/ncm-batch-converter-gui.git
   ```

2. Navigate to the script's directory:
   ```Bash
   cd ncm-batch-converter-gui
   ```
3. Install dependencies
   ```Bash
   pip install -r requirements.txt
   ```
### Usage

GUI Mode (Recommended for beginners):
```Bash
python3 main.py
```
Command-line Mode (Advanced):
```Bash
python3 ncm_converter.py /path/to/ncm/files [/path/to/output/folder]
```

If no output folder is specified, the converted files will be saved in the current working directory.

### License Compliance

- Original project (V1.0): MIT License
- Current version (V2.0): GNU General Public License v3.0
- All modifications comply with GPL-3.0-or-later terms
- Source code must remain open when distributing modified versions

### Contributing

Welcome contributions via [GitHub Issues](https://github.com/trustedinster/ncm-batch-converter-gui/issues). Please note:
1. All contributions must be licensed under GPL-3.0-or-later
2. Must preserve original copyright notices
3. Must include source code when distributing binaries

---

<a name="中文"></a>
## 中文

这是基于原始MIT协议项目的二次开发GUI版本，已升级为符合GPL-3.0-or-later协议的图形界面工具。

### 功能特性

- 🖥️ 双模式支持:
- - 命令行模式：python3 ncm_converter.py
- - GUI模式：python3 main.py (带有进度条和错误处理)
- 🔁 NCM文件批量转换MP3/FLAC
- 📄 保留元数据（标题、艺术家、专辑）
- 🎨 保留专辑封面
- 📊 实时转换进度追踪
- 📋 详细日志记录（保存在.\log\目录）

### 环境要求

- Python 3.14+（推荐)
- pip（Python 包安装器）
- tkinter（标准Python发行版自带）

以及以下第三方依赖：
- pycryptodome
- mutagen

### 安装

1. 克隆此仓库：
   ```Bash
   git clone https://github.com/trustedinster/ncm-batch-converter-gui.git
   ```

2. 进入脚本所在目录：
   ```Bash
   cd ncm-batch-converter-gui
   ```
3. 安装依赖
   ```Bash
   pip install -r requirements.txt
   ```

### 使用方法

图形界面模式 (推荐新手使用):
```Bash
python3 main.py
```
命令行模式 (高级用户):
```Bash
python3 ncm_converter.py /path/to/ncm/files [/path/to/output/folder]
```


如果没有指定输出文件夹，转换后的文件将保存在当前工作目录中。

### 许可证合规

- 原始项目 (V1.0)：MIT协议
- 当前版本 (V2.0)：GNU通用公共许可证v3.0
- 所有修改必须遵循GPL-3.0-or-later条款
- 分发修改版本时必须保持源代码开放

### 贡献

欢迎通过 [GitHub Issues](https://github.com/trustedinster/ncm-batch-converter-gui/issues) 提交贡献，请注意：
1. 所有贡献必须使用GPL-3.0-or-later协议
2. 必须保留原始版权声明
3. 分发二进制文件时必须包含源代码

### 特别声明
本软件仅限个人学习使用，使用后请在24小时内删除，请勿用于商业用途。请遵守《中华人民共和国著作权法》及相关法律法规，尊重音乐版权方的合法权益。