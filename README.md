# 暗黑破坏神2 恐怖地带追踪器

## 项目简介

这是一个用于追踪暗黑破坏神2（Diablo II Resurrected）恐怖地带（Terror Zones）信息的工具。该工具通过抓取外部网站数据，提供实时的恐怖地带信息，包括当前和下场恐怖地带的详细信息，并记录历史数据。

## 功能特性

- **实时恐怖地带信息**：获取当前和下场恐怖地带的详细信息
- **多语言支持**：优先显示简体中文，支持繁体中文和英文
- **场景位置识别**：自动识别恐怖地带所属的游戏章节
- **属性免疫信息**：显示场景的属性免疫情况
- **历史记录**：记录最近24小时的恐怖地带刷新记录
- **Web界面**：提供美观的Web界面，支持响应式设计
- **API接口**：提供RESTful API接口，方便其他应用集成
- **定时任务**：自动定时更新恐怖地带数据
- **Docker支持**：提供Docker部署方案

## 技术栈

- **后端**：Python 3.x, Flask
- **数据抓取**：requests, BeautifulSoup4
- **前端**：HTML5, CSS3, JavaScript
- **数据存储**：JSON文件
- **容器化**：Docker, Docker Compose

## 项目结构

```
getD2rTzInfo/
├── app.py              # 主应用文件，包含Flask服务器和核心功能
├── get_tz_data.py      # 数据获取脚本
├── get_tz_info.py      # 恐怖地带信息抓取类
├── index.html          # 前端Web界面
├── navigation.json     # 导航链接配置
├── tz_history.json     # 恐怖地带历史记录
├── docker-compose.yml  # Docker Compose配置
├── Dockerfile          # Docker构建文件
└── .gitignore          # Git忽略文件
```

## 安装与运行

### 方法一：直接运行

1. **安装依赖**
   ```bash
   pip install flask requests beautifulsoup4 schedule
   ```

2. **运行应用**
   ```bash
   python app.py
   ```

3. **访问界面**
   打开浏览器访问 `http://localhost:15554`

### 方法二：Docker部署

1. **构建并运行容器**
   ```bash
   docker-compose up -d
   ```

2. **访问界面**
   打开浏览器访问 `http://localhost:15554`

## API接口

### 1. 获取恐怖地带信息

**URL**: `/api/terror-zones`

**方法**: GET

**响应示例**:
```json
{
  "current": {
    "name": "干燥高地",
    "immunities": ["Fire", "Lightning"],
    "location": "Act 2",
    "time": "2026-03-06 15:00:00"
  },
  "next": {
    "name": "亡者大殿",
    "immunities": ["Cold", "Poison"],
    "location": "Act 2",
    "time": "2026-03-06 15:30:00"
  }
}
```

### 2. 获取历史记录

**URL**: `/api/tz-history`

**方法**: GET

**响应示例**:
```json
{
  "records": [
    {
      "timestamp": "2026-03-06T15:03:00",
      "name": "干燥高地",
      "location": "Act 2",
      "immunities": ["Fire", "Lightning"],
      "time": "2026-03-06 15:00:00"
    }
  ]
}
```

## 使用说明

1. **Web界面**：打开应用后，首页会显示当前和下场恐怖地带的详细信息，包括场景名称、位置、属性免疫和时间信息。

2. **刷新数据**：点击"刷新数据"按钮可以手动更新恐怖地带信息。

3. **历史记录**：页面下方显示最近24小时的恐怖地带刷新记录，按时间倒序排列。

4. **导航链接**：页面顶部提供相关工具的导航链接，可通过编辑 `navigation.json` 文件自定义。

## 数据来源

本工具从 [d2emu.com](https://d2emu.com/tz) 网站抓取恐怖地带信息，数据仅供参考。

## 注意事项

1. **网络连接**：使用前请确保网络连接正常，能够访问外部网站。

2. **数据准确性**：恐怖地带信息来源于外部网站，可能存在延迟或误差。

3. **定时任务**：应用会每小时的3分和33分自动更新数据，每天00:00清理过期记录。

4. **数据存储**：历史记录默认只保留最近24小时的数据，存储在 `tz_history.json` 文件中。

5. **端口配置**：默认使用15554端口，可在 `app.py` 文件中修改。

## 自定义配置

### 导航链接

编辑 `navigation.json` 文件可以自定义顶部导航链接：

```json
[
  {"name": "暗黑破坏神2", "address": "https://diablo2.blizzard.com/"},
  {"name": "d2emu", "address": "https://d2emu.com/"}
]
```

### 场景位置映射

在 `app.py` 文件中的 `_extract_location` 方法中可以扩展场景位置映射关系，添加新的场景名称和对应的游戏章节。

## 故障排除

1. **无法获取数据**：检查网络连接，确保能够访问 d2emu.com 网站。

2. **数据显示异常**：可能是网站结构发生变化，需要更新抓取逻辑。

3. **Docker运行失败**：检查Docker环境是否正常，查看容器日志获取详细错误信息。

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request，帮助改进这个项目。

## 联系方式

如有问题或建议，可通过以下方式联系：
- GitHub: [lilei19910122](https://github.com/lilei19910122)
