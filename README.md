# 舆情大数据服务

[该MCP服务提供企业舆情大数据分析功能，包括舆情情感统计分析、相关新闻列表查询等，帮助企业实时监控网络舆情动态，分析公众情感倾向，为企业声誉管理和公关决策提供数据支持。](https://www.handaas.com/)

## 服务特色

🚀 **实时舆情监控** - 基于海量互联网数据，实时追踪企业相关舆情信息  
📈 **情感分析** - 智能分析舆情情感倾向，包括正面、负面、中性、未知四个维度  
🔍 **精准搜索** - 支持企业名称、统一社会信用代码、注册号等多种检索方式  
📊 **趋势分析** - 提供舆情情感变化趋势，帮助企业把握舆论走向  
🎯 **分类筛选** - 支持按情感类别筛选新闻，快速定位关键信息

## 主要功能

- 🔍 **企业关键词模糊搜索** - 根据关键词快速找到相关企业基础信息
- 📊 **企业舆情情感统计** - 分析企业舆情的情感分布和趋势变化
- 📄 **企业舆情新闻列表查询** - 获取企业相关的详细新闻舆情信息

## 环境要求

- Python 3.10+
- 依赖包：python-dotenv, requests, mcp

## 本地快速启动

### 1. 克隆项目
```bash
git clone https://github.com/handaas/news-mcp-server
cd news-mcp-server
```

### 2. 创建虚拟环境&安装依赖

```bash
python -m venv mcp_env && source mcp_env/bin/activate
pip install -r requirements.txt
```

### 3. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下环境变量：

```env
INTEGRATOR_ID=your_integrator_id
SECRET_ID=your_secret_id
SECRET_KEY=your_secret_key
```

### 4. streamable-http启动服务

```bash
python server/mcp_server.py streamable-http
```

服务将在 `http://localhost:8000` 启动。

#### 支持启动方式 stdio 或 sse 或 streamable-http

### 5. Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "news-mcp-server": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## STDIO版安装部署

### 设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "news-mcp-server": {
      "command": "uv",
      "args": ["run", "mcp", "run", "{workdir}/server/mcp_server.py"],
      "env": {
        "PATH": "{workdir}/mcp_env/bin:$PATH",
        "PYTHONPATH": "{workdir}/mcp_env",
        "INTEGRATOR_ID": "your_integrator_id",
        "SECRET_ID": "your_secret_id",
        "SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

## 使用官方Remote服务

### 1. 直接设置Cursor / Cherry Studio MCP配置

```json
{
  "mcpServers": {
    "news-mcp-server":{
      "type": "streamableHttp",
      "url": "https://mcp.handaas.com/news/news_bigdata?token={token}"  
      }
  }
}
```

### 注意：integrator_id、secret_id、secret_key及token需要登录 https://www.handaas.com/ 进行注册开通平台获取


## 可用工具

### 1. news_bigdata_fuzzy_search
**功能**: 企业关键词模糊查询

根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。返回匹配的企业列表及其详细信息，用于查找和识别特定的企业信息。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 查询各类信息包含匹配关键词的企业
- `pageIndex` (可选): 分页开始位置
- `pageSize` (可选): 分页结束位置 - 一页最多获取50条数据

**返回值**:
- `total`: 总数
- `annualTurnover`: 年营业额
- `formerNames`: 曾用名
- `address`: 注册地址
- `foundTime`: 成立时间
- `enterpriseType`: 企业主体类型
- `legalRepresentative`: 法定代表人
- `homepage`: 企业官网
- `legalRepresentativeId`: 法定代表人id
- `prmtKeys`: 推广关键词
- `operStatus`: 企业状态
- `logo`: 企业logo
- `nameId`: 企业id
- `regCapitalCoinType`: 注册资本币种
- `regCapitalValue`: 注册资本金额
- `name`: 企业名称
- `catchReason`: 命中原因 - 包含企业名称、曾用名、股东、招聘岗位、地址、品牌、产品名称、固话、邮箱、手机、专利、资质证书、推广关键词、统一社会信用代码等信息

### 2. news_bigdata_news_stats
**功能**: 企业舆情情感统计

根据输入的企业标识信息（如名称、注册号等），查询并统计该企业的舆情情感类型，包括消极、中立、积极、和未知四类情感的分布及其趋势变化。主要用于企业的声誉管理和舆情监控，帮助企业了解社会对其的评价和情绪变化趋势。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称
- `keywordType` (可选): 主体类型 - name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码

**返回值**:
- `newsSentimentStats`: 舆情情感类型统计 - neutral：中立，negative：消极，positive：积极，unknown：未知
- `sentimentLabelList`: 所有舆情类别列表 - neutral：中立，negative：消极，positive：积极
- `newsSentimentTrend`: 舆情趋势
  - `month`: 月份 - 格式：yyyy-mm
  - `stats`: 情感类型 - negative：消极，positive：积极

### 3. news_bigdata_news_list
**功能**: 企业舆情新闻列表查询

通过企业的基本标识信息或企业ID及指定舆情类别，查询并返回与该企业相关的新闻舆情信息明细，包括新闻简介、链接、发布时间、来源、标题、相关企业等详细内容以及舆情的分类和总数量。适用于企业风险管理、市场竞争分析、公关策略制定等场景。

**参数**:
- `matchKeyword` (必需): 匹配关键词 - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称
- `keywordType` (可选): 主体类型 - name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码
- `pageIndex` (可选): 页码 - 从1开始，默认为1
- `pageSize` (可选): 分页大小 - 一页最多获取50条，默认为50
- `sentimentLabel` (可选): 舆情类别 - 0：负面，1：正面，2：中性，3：未知

**返回值**:
- `newsBrief`: 新闻简介
- `newsLink`: 新闻链接
- `newsPublishTime`: 新闻发布时间
- `newsSource`: 新闻来源
- `newsTitle`: 新闻标题
- `relatedEnterprises`: 相关企业列表
- `sentimentLabel`: 舆情类别 - 0：负面，1：正面，2：中性，3：未知

## 应用场景

### 🛡️ 企业风险预警
- **舆情监控**: 24/7实时监控企业相关舆情，第一时间发现负面信息
- **预警机制**: 通过情感分析及时识别舆情风险，提前制定应对措施
- **危机管控**: 负面事件发生时，快速获取舆情全貌，制定精准应对策略

### 📊 品牌声誉管理  
- **声誉评估**: 定期分析企业舆情情感分布，评估品牌声誉健康度
- **形象监控**: 跟踪品牌在不同媒体渠道的形象变化趋势
- **口碑分析**: 分析用户对企业产品和服务的真实反馈

### 🎯 公关策略优化
- **效果评估**: 评估公关活动的舆情效果和公众反响
- **策略调整**: 基于舆情数据调整公关传播策略和内容方向
- **媒体关系**: 分析不同媒体对企业的报道倾向

### 🔍 竞争情报分析
- **对手监控**: 监控竞争对手的舆情表现和市场声誉
- **行业洞察**: 了解行业内企业的舆情表现，发现市场机会
- **基准比较**: 与同行业企业进行舆情表现对比分析

### 💼 投资决策支持
- **尽职调查**: 为投资决策提供目标企业的舆情背景调查
- **风险评估**: 评估投资标的的舆情风险和声誉风险
- **市场情绪**: 分析市场对特定企业或行业的情绪变化

## 使用注意事项

1. **企业全称要求**: 在调用需要企业全称的接口时，如果没有企业全称则先调取news_bigdata_fuzzy_search接口获取企业全称
2. **分页限制**: 一页最多获取50条数据
3. **舆情类别**: 支持按情感类型进行筛选查询（负面、正面、中性、未知）
4. **关键词类型**: 支持多种企业标识方式（企业名称、企业id、注册号、统一社会信用代码）

## 使用提问示例

### 🔍 企业关键词模糊搜索 (news_bigdata_fuzzy_search)
```
1. "帮我查找包含'华为'关键词的企业信息"
2. "搜索与'新能源汽车'相关的企业列表"  
3. "查询名称中包含'科技'的公司，获取前20条"
4. "找一下'比亚迪'相关的企业基础信息"
```

### 📊 企业舆情情感统计 (news_bigdata_news_stats)
```
1. "华为技术有限公司的舆情情感分布如何？最近趋势怎样？"
2. "分析一下腾讯控股有限公司的舆情情感统计"
3. "比亚迪股份有限公司最近的舆情情感变化趋势"
4. "查询阿里巴巴集团的舆情情感分布数据"
```

### 📄 企业舆情新闻列表查询 (news_bigdata_news_list)
```
1. "查询华为技术有限公司最近的舆情新闻"
2. "搜索苹果公司的负面舆情信息，显示详细内容"
3. "获取腾讯最近的正面新闻报道，要20条"
4. "查找小米集团的中性舆情新闻"
5. "获取比亚迪最近50条舆情新闻，包括新闻来源和发布时间"
6. "查看特斯拉相关的负面舆情新闻列表"
```

### 💡 综合分析示例
```
1. "帮我全面分析一下'蔚来汽车'的舆情状况，包括情感分布和最新新闻"
2. "我想了解'字节跳动'的舆情表现，先查企业信息，再看情感统计和新闻"
3. "请分析'美团'的舆情风险，重点关注负面新闻"
``` 