# ManageBac Assignment Checker

一个用于自动检查ManageBac作业的Python工具，支持多种报告格式和通知功能。

## 功能特性

- 🔍 自动登录ManageBac并抓取作业信息
- - 📊 生成多种格式的报告（HTML、Markdown、JSON、控制台）
  - - 📧 邮件通知功能
    - - 🎯 智能优先级和紧急程度分析
      - - 📈 详细的统计分析和可视化
        - - ⚙️ 灵活的配置选项
          - - 🧪 完整的单元测试覆盖
           
            - ## 快速开始
           
            - ### 安装
           
            - ```bash
              # 克隆仓库
              git clone https://github.com/Hacker0458/managebac-assignment-checker.git
              cd managebac-assignment-checker

              # 安装依赖
              pip install -r requirements.txt

              # 或者使用setup.py安装
              pip install -e .
              ```

              ### 配置

              1. 复制环境变量模板：
              2. ```bash
                 cp .env.example .env
                 ```

                 2. 编辑`.env`文件，填入您的ManageBac凭据：
                 3. ```env
                    MANAGEBAC_EMAIL=your_email@example.com
                    MANAGEBAC_PASSWORD=your_password
                    MANAGEBAC_URL=https://your-school.managebac.com
                    ```

                    ### 使用

                    ```bash
                    # 基本使用
                    python main_new.py

                    # 使用命令行接口
                    python -m managebac_checker.cli --help

                    # 指定报告格式
                    python -m managebac_checker.cli --format html
                    ```

                    ## 项目结构

                    ```
                    managebac-assignment-checker/
                    ├── managebac_checker/          # 主要代码包
                    │   ├── __init__.py
                    │   ├── config.py              # 配置管理
                    │   ├── scraper.py             # 网页抓取
                    │   ├── analyzer.py            # 数据分析
                    │   ├── reporter.py            # 报告生成
                    │   ├── checker.py             # 主检查器
                    │   ├── notifications.py       # 通知功能
                    │   └── cli.py                 # 命令行接口
                    ├── tests/                     # 单元测试
                    ├── .github/workflows/         # CI/CD配置
                    ├── setup.py                   # 安装配置
                    ├── requirements.txt           # 依赖列表
                    ├── README.md                  # 项目说明
                    └── LICENSE                    # 许可证
                    ```

                    ## 开发

                    ### 运行测试

                    ```bash
                    pytest tests/
                    ```

                    ### 代码格式化

                    ```bash
                    black managebac_checker/
                    flake8 managebac_checker/
                    ```

                    ## 许可证

                    本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

                    ## 贡献

                    欢迎提交Issue和Pull Request！

                    ## 注意事项

                    - 请确保您有权限访问ManageBac系统
                    - - 请遵守学校的使用条款和隐私政策
                      - - 建议在测试环境中先验证功能
