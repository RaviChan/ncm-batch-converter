# NCM to MP3/FLAC Converter | NCM 转 MP3/FLAC 转换器

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

This Python script allows you to batch convert Netease Cloud Music (.ncm) files to standard audio formats (MP3/FLAC) while preserving metadata and album art.

### Features

- Batch conversion of NCM files to MP3 or FLAC format
- Preserves original metadata (title, artist, album)
- Retains album artwork
- Automatically installs required dependencies
- Simple command-line interface

### Requirements

- Python 3.6+
- pip (Python package installer)

The script will automatically install the following dependencies if they are not present:
- pycryptodome
- mutagen

### Installation

1. Clone this repository or download the script:
   ```
   git clone https://github.com/your-username/ncm-converter.git
   ```
   or download `ncm_converter.py` directly.

2. Navigate to the script's directory:
   ```
   cd ncm-converter
   ```

### Usage

Run the script from the command line, providing the path to the folder containing NCM files:

```
python3 ncm_converter.py /path/to/ncm/files
```

The converted files will be saved in the current working directory.

### Note

This script is for personal use only. Please ensure you have the right to convert and use these music files. Respect copyright laws and terms of service of music providers.

### Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/your-username/ncm-converter/issues) if you want to contribute.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="中文"></a>
## 中文

这个 Python 脚本允许您批量将网易云音乐 (.ncm) 文件转换为标准音频格式（MP3/FLAC），同时保留元数据和专辑封面。

### 功能特性

- 批量将 NCM 文件转换为 MP3 或 FLAC 格式
- 保留原始元数据（标题、艺术家、专辑）
- 保留专辑封面
- 自动安装所需依赖
- 简单的命令行界面

### 环境要求

- Python 3.6+
- pip（Python 包安装器）

如果以下依赖不存在，脚本将自动安装：
- pycryptodome
- mutagen

### 安装

1. 克隆此仓库或下载脚本：
   ```
   git clone https://github.com/your-username/ncm-converter.git
   ```
   或直接下载 `ncm_converter.py` 文件。

2. 进入脚本所在目录：
   ```
   cd ncm-converter
   ```

### 使用方法

从命令行运行脚本，提供包含 NCM 文件的文件夹路径：

```
python3 ncm_converter.py /path/to/ncm/files
```

转换后的文件将保存在当前工作目录中。

### 注意事项

此脚本仅供个人使用。请确保您有权转换和使用这些音乐文件。请遵守版权法和音乐提供商的服务条款。

### 贡献

欢迎贡献、提出问题和功能请求。如果您想贡献，请查看 [issues 页面](https://github.com/your-username/ncm-converter/issues)。

### 许可证

该项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。

