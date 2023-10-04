// 导入模块
const express = require('express')
const app = express()

// 连接数据库
const mysql = require('mysql')
const conn = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'123456',
    port:'3306',
    database:'qhcps_database'
})
conn.connect()

// 路由 get_qh_data -> 获取期货表格数据 返回值 -> json
app.get("/get_qh_data",function(req,res){
    
    // sql 语句
    let sql = 'select * from deal order by stars desc'

    // 执行 sql 语句
    conn.query(sql,function(err,result){
        // console.log(result[0].id)
        data_list = []

        // 遍历查询结果并插入到 data_list 
        for(let i=0;i<result.length;i++){
            data = {
                no:i,
                id:result[i].id,
                username: result[i].username,
                latest_equity: result[i].latest_equity,
                avg_equity: result[i].avg_equity,
                cumulative_net_profit: result[i].cumulative_net_profit,
                annual_net_profit_margin: result[i].annual_net_profit_margin,
                accumulated_handling_fees: result[i].accumulated_handling_fees,
                annual_handling_fee: result[i].annual_handling_fee,
                cumulative_net_worth: result[i].cumulative_net_worth,
                maximum_retracement_rate: result[i].maximum_retracement_rate,
                stars: result[i].stars
            }

            data_list.push(data)

        }
        res.header("Access-Control-Allow-Origin", "*") // 跨域
        res.json(data_list)
    })
    
})

// 路由 get_data_by_id -> 获取图表数据 返回值 -> json
app.get("/get_data_by_id",function(req,res){
    
    // 请求参数 id
    let id = req.query['id']

    // sql 语句
    let sql = `select * from deal_detail where id='${id}'`

    // 执行 sql 语句
    conn.query(sql,function(err,result){
        // console.log(result[0].id)

        dtime = [] // 时间
        cumulative_net_profit = [] // 累计净利润
        accumulated_handling_fees = [] // 累计手续费

        // 遍历查询结果并插入数据到 data 中
        for(let i=0;i<result.length;i++){
            let t = result[i].dtime
            dtime.push(String(t.getFullYear())+ "-" + String(t.getMonth())+ "-" + String(t.getDate()))
            cumulative_net_profit.push(result[i].cumulative_net_profit)
            accumulated_handling_fees.push(result[i].accumulated_handling_fees)
        }

        // 返回值
        data = {
            id:id,
            dtime:dtime,
            cumulative_net_profit:cumulative_net_profit,
            accumulated_handling_fees:accumulated_handling_fees
        }
        
        res.header("Access-Control-Allow-Origin", "*") // 跨域
        res.json(data)
    })
    
})

// 启动服务器
app.listen(9527,()=>{
    console.log("server running at http://127.0.0.1:9527")
})