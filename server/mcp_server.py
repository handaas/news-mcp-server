# 全局导入
import json
import os
from hashlib import md5
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys

load_dotenv()

mcp = FastMCP("舆情大数据", instructions="舆情大数据", dependencies=["python-dotenv", "requests"])

INTEGRATOR_ID = os.environ.get("INTEGRATOR_ID")
SECRET_ID = os.environ.get("SECRET_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")

def call_api(product_id: str, params: dict) -> dict:
    """
    调用API接口
    
    参数:
      - product_id: 数据产品ID
      - params: 接口参数
    
    返回:
      - 接口返回的JSON数据
    """
    if not params:
        params = {}
    
    if not INTEGRATOR_ID:
        return {"error": "对接器ID不能为空"}
    
    if not SECRET_ID:
        return {"error": "密钥ID不能为空"}
    
    if not SECRET_KEY:
        return {"error": "密钥不能为空"}
    
    if not product_id:
        return {"error": "产品ID不能为空"}
    
    call_params = {
        "product_id": product_id,
        "secret_id": SECRET_ID,
        "params": json.dumps(params, ensure_ascii=False)
    }
    
    # 生成签名
    keys = sorted(list(call_params.keys()))
    params_str = ""
    for key in keys:
        params_str += str(call_params[key])
    params_str += SECRET_KEY
    sign = md5(params_str.encode("utf-8")).hexdigest()
    call_params["signature"] = sign
    
    # 调用API
    url = f'https://console.handaas.com/api/v1/integrator/call_api/{INTEGRATOR_ID}'
    try:
        response = requests.post(url, data=call_params)
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("data", None) or response_json.get("msgCN", None) or response_json
        else:
            return f"接口调用失败，状态码：{response.status_code}"
    except Exception as e:
        return "查询失败"
    
@mcp.tool()
def news_bigdata_fuzzy_search(matchKeyword: str, pageIndex: int = 1, pageSize: int = 50) -> dict:
    """
    该接口的功能是根据提供的企业名称、人名、品牌、产品、岗位等关键词模糊查询相关企业列表。返回匹配的企业列表及其详细信息，用于查找和识别特定的企业信息。


    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 查询各类信息包含匹配关键词的企业
    - pageIndex: 分页开始位置 类型：int - 默认从1开始
    - pageSize: 分页结束位置 类型：int - 一页最多获取50条数据, 不能超过50, 超过50的统一用50代替

    返回参数:
    - total: 总数 类型：int
    - resultList:查询返回企业信息列表 类型：list of dict:
        - annualTurnover: 年营业额 类型：string
        - formerNames: 曾用名 类型：list of string
        - address: 注册地址 类型：string
        - foundTime: 成立时间 类型：string
        - enterpriseType: 企业主体类型 类型：string
        - legalRepresentative: 法定代表人 类型：string
        - legalRepresentativeId: 法定代表人id 类型：string
        - homepage: 企业官网 类型：string
        - prmtKeys: 推广关键词 类型：list of string
        - operStatus: 企业状态 类型：string
        - logo: 企业logo 类型：string
        - nameId: 企业id 类型：string
        - regCapitalCoinType: 注册资本币种 类型：string
        - regCapitalValue: 注册资本金额 类型：int
        - name: 企业名称 类型：string
        - catchReason: 命中原因 类型：dict
            - catchReason.name: 企业名称 类型：list of string
            - catchReason.formerNames: 曾用名 类型：list of string
            - catchReason.holderList: 股东 类型：list of string
            - catchReason.recruitingName: 招聘岗位 类型：list of string
            - catchReason.address: 地址 类型：list of string
            - catchReason.operBrandList: 品牌 类型：list of string
            - catchReason.goodsNameList: 产品名称 类型：list of string
            - catchReason.phoneList: 固话 类型：list of string
            - catchReason.emailList: 邮箱 类型：list of string
            - catchReason.mobileList: 手机 类型：list of string
            - catchReason.patentNameList: 专利 类型：list of string
            - catchReason.certNameList: 资质证书 类型：list of string
            - catchReason.prmtKeys: 推广关键词 类型：list of string
            - catchReason.socialCreditCode: 统一社会信用代码 类型：list of string
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('675cea1f0e009a9ea37edaa1', params)


@mcp.tool()
def news_bigdata_news_stats(matchKeyword: str, keywordType: str = None) -> dict:
    """
    该接口的功能是根据输入的企业标识信息（如名称、注册号等），查询并统计该企业的舆情情感类型，包括消极、中立、积极、和未知四类情感的分布及其趋势变化。该接口主要用于企业的声誉管理和舆情监控，帮助企业了解社会对其的评价和情绪变化趋势，从而在公关、市场策略调整、风险预警等方面进行及时决策。适用场景包括企业需要进行危机公关时，分析特定时期内的舆情变化；或在日常进行品牌形象监控，判断市场对公司行为或决策的反应等。

    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码)

    返回参数:
    - newsSentimentStats: 舆情情感类型统计 类型：dict - neutral：中立，negative：消极，positive：积极，unknown：未知
    - sentimentLabelList: 所有舆情类别列表 类型：list of string - neutral：中立，negative：消极，positive：积极
    - newsSentimentTrend: 舆情趋势 类型：dict
        - month: 月份 类型：string - 格式：yyyy-mm
        - stats: 情感类型 类型：dict - negative：消极，positive：积极
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66b338e274bf098447db7efd', params)


@mcp.tool()
def news_bigdata_news_list(matchKeyword: str, keywordType: str = None, pageIndex: int = 1, pageSize: int = 50, sentimentLabel: int = None) -> dict:
    """
    该接口的功能是通过企业的基本标识信息或企业ID及指定舆情类别，查询并返回与该企业相关的新闻舆情信息明细，包括新闻简介、链接、发布时间、来源、标题、相关企业等详细内容以及舆情的分类和总数量。此接口可广泛应用于企业风险管理、市场竞争分析、公关策略制定等场景，帮助企业或相关机构快速掌握企业动态、社会声誉及潜在风险，通过对舆情类别的筛选和分析来进行有效决策和战略调整。

    请求参数:
    - matchKeyword: 匹配关键词 类型：string - 企业名称/注册号/统一社会信用代码/企业id，如果没有企业全称则先调取fuzzy_search接口获取企业全称。
    - keywordType: 主体类型 类型：select - 主体类型枚举（name：企业名称，nameId：企业id，regNumber：注册号，socialCreditCode：统一社会信用代码)
    - pageIndex: 页码 类型：int - 默认从1开始
    - pageSize: 分页大小 类型：int - 一页最多获取50条数据, 不能超过50, 超过50的统一用50代替
    - sentimentLabel: 舆情类别 类型：int - 舆情类别枚举（0：负面，1：正面，2：中性，3：未知）


    返回参数:
    - resultList: 结果列表 类型：list of dict
        - newsBrief: 新闻简介 类型：string
        - newsLink: 新闻链接 类型：string
        - newsPublishTime: 新闻发布时间 类型：string
        - newsSource: 新闻来源 类型：string
        - newsTitle: 新闻标题 类型：string
        - relatedEnterprises: 相关企业列表 类型：list of dict
        - sentimentLabel: 舆情类别 类型：int - 舆情类别枚举（0：负面，1：正面，2：中性，3：未知）
    - total: 总数 类型：int
    """
    # 构建请求参数
    params = {
        'matchKeyword': matchKeyword,
        'keywordType': keywordType,
        'pageIndex': pageIndex,
        'pageSize': pageSize,
        'sentimentLabel': sentimentLabel
    }

    # 过滤None值
    params = {k: v for k, v in params.items() if v is not None}

    # 调用API
    return call_api('66b485eadaf8c77fb249a455', params)

if __name__ == "__main__":
    print("正在启动MCP服务...")
    # 解析第一个参数
    if len(sys.argv) > 1:
        start_type = sys.argv[1]
    else:
        start_type = "stdio"

    print(f"启动方式: {start_type}")
    if start_type == "stdio":
        print("正在使用stdio方式启动MCP服务器...")
        mcp.run(transport="stdio")
    if start_type == "sse":
        print("正在使用sse方式启动MCP服务器...")
        mcp.run(transport="sse")
    elif start_type == "streamable-http":
        print("正在使用streamable-http方式启动MCP服务器...")
        mcp.run(transport="streamable-http")
    else:
        print("请输入正确的启动方式: stdio 或 sse 或 streamable-http")
        exit(1)
    