#!/bin/bash

# 高光谱图像分类综述文档编译脚本
# Compilation script for Hyperspectral Image Classification Review

echo "开始编译高光谱图像分类综述文档..."
echo "Starting compilation of HSI classification review document..."

# 检查必要文件是否存在
if [ ! -f "hsi_classification_review_en.tex" ]; then
    echo "错误: 找不到主文档文件 hsi_classification_review_en.tex"
    echo "Error: Main document file hsi_classification_review_en.tex not found"
    exit 1
fi

if [ ! -f "references.bib" ]; then
    echo "错误: 找不到参考文献文件 references.bib"
    echo "Error: Bibliography file references.bib not found"
    exit 1
fi

# 清理之前的编译文件
echo "清理之前的编译文件..."
echo "Cleaning previous compilation files..."
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

# 第一次编译 - 生成辅助文件
echo "第一次编译 (生成辅助文件)..."
echo "First compilation (generating auxiliary files)..."
pdflatex -interaction=nonstopmode hsi_classification_review_en.tex

if [ $? -ne 0 ]; then
    echo "错误: 第一次编译失败"
    echo "Error: First compilation failed"
    exit 1
fi

# 编译参考文献
echo "编译参考文献..."
echo "Compiling bibliography..."
bibtex hsi_classification_review_en

if [ $? -ne 0 ]; then
    echo "警告: BibTeX编译可能有问题，但继续进行..."
    echo "Warning: BibTeX compilation may have issues, but continuing..."
fi

# 第二次编译 - 处理引用
echo "第二次编译 (处理引用)..."
echo "Second compilation (processing references)..."
pdflatex -interaction=nonstopmode hsi_classification_review_en.tex

if [ $? -ne 0 ]; then
    echo "错误: 第二次编译失败"
    echo "Error: Second compilation failed"
    exit 1
fi

# 第三次编译 - 确保所有引用正确
echo "第三次编译 (确保引用正确)..."
echo "Third compilation (ensuring correct references)..."
pdflatex -interaction=nonstopmode hsi_classification_review_en.tex

if [ $? -ne 0 ]; then
    echo "错误: 第三次编译失败"
    echo "Error: Third compilation failed"
    exit 1
fi

# 检查输出文件
if [ -f "hsi_classification_review_en.pdf" ]; then
    echo "编译成功! PDF文件已生成: hsi_classification_review_en.pdf"
    echo "Compilation successful! PDF file generated: hsi_classification_review_en.pdf"

    # 显示文件大小
    file_size=$(ls -lh hsi_classification_review_en.pdf | awk '{print $5}')
    echo "文件大小: $file_size"
    echo "File size: $file_size"
else
    echo "错误: PDF文件未生成"
    echo "Error: PDF file not generated"
    exit 1
fi

# 可选: 清理编译过程中的临时文件
read -p "是否清理临时文件? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "清理临时文件..."
    echo "Cleaning temporary files..."
    rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz
    echo "临时文件已清理"
    echo "Temporary files cleaned"
fi

echo "编译完成!"
echo "Compilation completed!"
