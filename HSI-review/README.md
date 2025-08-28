# HSI-review 项目整理说明

## 项目结构

```
HSI-review/
├── hsi_classification_review_en.tex    # 主要的LaTeX文档（英文版）
├── references.bib                      # 外部参考文献数据库
├── compile.sh                          # 编译脚本
├── IEEEtran.cls                        # IEEE期刊模板类文件
├── 研究计划.md                         # 研究计划文档
├── 综述草稿.md                         # 综述草稿
└── [编译生成的文件]                    # PDF和辅助文件
```

## 主要改进

### 1. 外部引用整理
- ✅ 移除了手动的 `\begin{thebibliography}` 环境
- ✅ 使用外部 `references.bib` 文件管理所有引用
- ✅ 在文档中添加了适当的 `\cite{}` 引用
- ✅ 配置了正确的 `\bibliographystyle{plain}` 和 `\bibliography{references}`

### 2. 引用数据库 (references.bib)
包含了460个高质量的参考文献，涵盖：
- 传统机器学习方法 (SVM, Random Forest等)
- 深度学习方法 (CNN, RNN, Transformer等)
- 最新的State Space Models (Mamba架构)
- Foundation Models和自监督学习
- 跨域少样本学习
- 图神经网络方法
- 混合架构和新兴趋势

### 3. 编译脚本更新
- ✅ 更新了文件名引用 (`hsi_classification_review_en.tex`)
- ✅ 使用 `pdflatex` 替代 `xelatex`
- ✅ 正确的编译流程：LaTeX → BibTeX → LaTeX → LaTeX

## 使用方法

### 编译文档
```bash
# 方法1：使用编译脚本（推荐）
./compile.sh

# 方法2：手动编译
pdflatex hsi_classification_review_en.tex
bibtex hsi_classification_review_en
pdflatex hsi_classification_review_en.tex
pdflatex hsi_classification_review_en.tex
```

### 添加新引用
1. 在 `references.bib` 文件中添加新的BibTeX条目
2. 在LaTeX文档中使用 `\cite{key}` 引用
3. 重新编译文档

### 引用示例
```latex
传统方法如SVM \cite{melgani2004classification} 和Random Forest \cite{gislason2006random}
深度学习方法包括CNN \cite{chen2019deep} 和Transformer \cite{hong2021spectralformer}
最新的Mamba架构 \cite{zhu2024mambahsi} 显示了优异的性能
```

## 文档特点

### 内容覆盖
- 📊 400+ 篇2019-2024年的高质量论文
- 🔬 传统方法到最新深度学习架构的全面综述
- 📈 15个基准数据集的性能比较
- 🚀 新兴技术如Mamba、Foundation Models的深入分析

### 技术亮点
- 🎯 系统性的方法分类和比较
- 📋 详细的数据集描述和特征分析
- 🔍 计算效率和实际部署考虑
- 🌟 未来研究方向的识别

## 编译要求

### 必需软件
- LaTeX发行版 (TeX Live 2022+)
- BibTeX
- pdflatex

### 必需包
- IEEEtran (文档类)
- amsmath, amsfonts, amssymb (数学符号)
- graphicx (图形支持)
- cite (引用管理)
- hyperref (超链接)
- 其他标准LaTeX包

## 故障排除

### 常见问题
1. **引用未显示**: 确保运行了完整的编译流程 (LaTeX → BibTeX → LaTeX → LaTeX)
2. **BibTeX错误**: 检查 `references.bib` 文件格式是否正确
3. **编译失败**: 确保所有必需的LaTeX包已安装

### 编译输出
成功编译后会生成：
- `hsi_classification_review_en.pdf` - 最终PDF文档
- 各种辅助文件 (.aux, .bbl, .blg等)

## 维护说明

### 定期更新
- 添加最新的研究论文到 `references.bib`
- 更新文档内容以反映最新进展
- 检查和修正引用格式

### 版本控制
建议使用Git管理文档版本，特别注意：
- 跟踪 `.tex` 和 `.bib` 文件的变更
- 可以忽略编译生成的辅助文件
- 保留重要的PDF版本

---

**整理完成时间**: 2025年1月
**文档状态**: ✅ 已完成外部引用整理，可正常编译使用
