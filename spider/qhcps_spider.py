import requests
import pymysql
import time

from lxml import etree

# 连接数据库
conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='qhcps_database',
        charset='utf8'
    )

cursor = conn.cursor()

file_log = str(time.time()) # 时间戳

# 获取 qhcps 网页源码
def get_qhcps_data():
    
    # 请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.qhcps.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    
    # 响应数据
    response = requests.get("http://www.qhcps.com/",headers=headers)
    
    return response.text

# 解析数据
def analysis_data(data):
    
    # 使用 xpath 解析数据    
    tree = etree.HTML(data)
    trs = tree.xpath('//*[@id="processTbody"]/tr')[1:-1] # 获取 tbody 下所有 tr(剔除第一个)
    
    # 输出日志
    print("总计待爬取:%d个" % len(trs))
    log("总计待爬取:%d个" % len(trs))
    
    current = 0 # 索引
    for tr in trs:
        
        tds = tr.xpath("./td") # 获取 tr 下所有 td
        print("username:"+tr.xpath("./@username")[0]) # 用户名
        
        '''
        print("id:"+tr.xpath("./@value")[0]) # value 请求id
        print("username:"+tr.xpath("./@username")[0]) # 用户名
        print("最新权益:"+tds[2].xpath("./text()")[0])
        print("平均权益:"+tds[3].xpath("./text()")[0])
        print("累计净利润:"+tds[4].xpath("./text()")[0])
        print("年净利润率:"+tds[5].xpath("./text()")[0])
        print("累计手续费:"+tds[6].xpath("./text()")[0])
        print("年手续费率:"+tds[7].xpath("./text()")[0])
        print("累计净值:"+tds[8].xpath("./text()")[0])
        print("最大回撤率:"+tds[9].xpath("./text()")[0])
        print("本站评分:" + str(len(tds[10].xpath("./img"))))
        '''

        id = tr.xpath("./@value")[0] # id
        username = tr.xpath("./@username")[0] # 用户名
        latest_equity = tds[2].xpath("./text()")[0] # 最新权益
        avg_equity = tds[3].xpath("./text()")[0] # 平均权益
        cumulative_net_profit = tds[4].xpath("./text()")[0] # 累计净利润
        annual_net_profit_margin = tds[5].xpath("./text()")[0] # 年净利润率
        accumulated_handling_fees = tds[6].xpath("./text()")[0] # 累计手续费
        annual_handling_fee = tds[7].xpath("./text()")[0] # 年手续费率
        cumulative_net_worth = tds[8].xpath("./text()")[0] # 累计净值
        maximum_retracement_rate = tds[9].xpath("./text()")[0] # 最大回撤率
        stars = str(len(tds[10].xpath("./img"))) # 评分
        
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        # 输出日志
        print("[{}][{}]id->{},username->{}".format(now,str(current),id,username))
        log("[{}][{}]id->{},username->{}".format(now,str(current),id,username))
        
        # sql 语句插入到 mysql 数据库中
        sql = "insert into deal values('{}','{}',{},{},{},{},{},{},{},{},{});".format(
            id,
            username,
            latest_equity,
            avg_equity,
            cumulative_net_profit,
            annual_net_profit_margin.replace("%",""),
            accumulated_handling_fees,
            annual_handling_fee.replace("%",""),
            cumulative_net_worth.replace("%",""),
            maximum_retracement_rate.replace("%",""),
            stars
            )
        
        # 异常处理 发生错误标记错误位置
        try:
            # 执行 sql 语句
            cursor.execute(sql)
            conn.commit()
        except:
            print("插入数据时发生错误! sql -> " + sql)
            log("插入数据时发生错误! sql -> " + sql)
        
        # 获取详细数据
        get_data_by_id(id)
        current += 1
        # time.sleep(1)
        
        
        
# 获取对应 id 时间序列数据        
def get_data_by_id(id):
    
    # 请求头
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '42',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.qhcps.com',
        'Origin': 'http://www.qhcps.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.qhcps.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # 请求参数
    data = {
        'ajax':'1',
        'stime':'0',
        'etime':'0',
        'group_id':'-6',
        'search':''
    }
    
    # 发送 post 请求
    response = requests.post("http://www.qhcps.com/table/money/{}".format(id),headers=headers,data=data)
    
    # 获取 json 数据
    json_data = response.json() # data 累计手续费 , data2 累计净利润 , label 时间 , xStep x轴步长?
    
    # 异常处理
    if json_data == {}:
        print("[错误]id->{}爬取失败".format(id))
        log("[错误]id->{}爬取失败".format(id))

    # 遍历数据并插入数据库
    for i in range(len(json_data['data'])):
        sql = "insert into deal_detail values('{}','{}',{},{})".format(id,json_data['label'][i],json_data['data2'][i],json_data['data'][i])
        
        # 异常处理 发生错误标记错误位置
        try:
            # 执行 sql 语句
            cursor.execute(sql)
            conn.commit()
        except:
            print("插入详细数据时发生错误! sql -> " + sql)
            log("插入详细数据时发生错误! sql -> " + sql)

# 写出日志信息
def log(v):
    # if os.path.exists('./spider/log/' + str(time.time())):
    with open('./spider/log/' + file_log + ".txt",'a+',encoding='utf-8') as f:
        f.write(v + "\n")

# 主入口
if __name__ == '__main__':
    start_time = time.time()
    analysis_data(get_qhcps_data())
    end_time = time.time()
    print("累计耗时->{}秒".format(str(end_time-start_time)))
    