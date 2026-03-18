# 知识库PDF转换指南

## 📁 待转换的文件

在【知识库】文件夹中有以下文件需要转换：

1. **Tartine bread (Chad Robertson) (z-library.sk, 1lib.sk, z-lib.sk).pdf** (17.84 MB)
2. **The Perfect Loaf The Craft  (Maurizio Leo).pdf** (16.12 MB)  
3. **如何驾驭开放式组织 Open Crumb Mastery (Trevor J. Wilson) (z-library.sk, 1lib.sk, z-lib.sk).pdf** (23.04 MB)

另外还有一个EPUB文件：
- **The Perfect Loaf  The Craft and Science of Sourdough Breads, Sweets, and More  A Baking Book (Maurizio Leo).epub** (12.83 MB)

## 🛠️ 推荐的转换方法

### 方法1：使用在线工具（最简单）

1. **Convertio** - https://convertio.co/zh/pdf-md/
   - 支持PDF转Markdown
   - 免费在线使用，无需安装
   - 操作简单，拖拽上传即可

2. **CloudConvert** - https://cloudconvert.com/pdf-to-md
   - 支持多种格式转换
   - 转换质量较好
   - 每天有免费额度

### 方法2：使用桌面软件

1. **Pandoc**（推荐）
   ```bash
   # 安装 Pandoc: https://pandoc.org/installing.html
   # 转换命令：
   pandoc input.pdf -o output.md
   ```

2. **Calibre**（适合EPUB转Markdown）
   - 下载：https://calibre-ebook.com/
   - 支持EPUB转多种格式
   - 可以批量转换

3. **Adobe Acrobat Pro**
   - 导出为文本格式，再手动转换为Markdown

### 方法3：使用Python脚本（技术用户）

需要安装以下库：
```bash
pip install pdfplumber pymupdf
```

然后使用专门的转换脚本。

## 📋 转换步骤建议

1. **优先转换PDF文件**
   - 先从较小的PDF开始测试
   - 验证转换效果

2. **处理EPUB文件**
   - EPUB转Markdown通常效果更好
   - 可以使用Calibre或Pandoc

3. **质量检查**
   - 检查转换后的Markdown格式
   - 修正格式错误
   - 添加适当的标题结构

## 🎯 转换后的文件命名

建议使用简洁的文件名：
- `Tartine_Bread.md`
- `The_Perfect_Loaf.md` 
- `Open_Crum_Mastery.md`

## 💡 提示

- PDF转换效果可能因文件质量而异
- 扫描版PDF需要OCR识别，效果较差
- 原版电子书PDF转换效果最好
- 转换后建议手动检查和修正格式

---

**准备好转换工具后，可以开始转换这些宝贵的烘焙知识库文件！**
