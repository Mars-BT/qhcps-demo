

<template>
  <!-- 导航栏 -->
  <Menu mode="horizontal" theme="light" active-name="1" @on-select="select_menu">

    <MenuItem name="1">
    <Icon type="md-analytics" />
    数据展示
    </MenuItem>

    <MenuItem name="2">
    <Icon type="md-archive" />
    代码展示/下载
    </MenuItem>

  </Menu>
  <br>

  <!-- 表格 -->
  <Table border :columns="columns" :data="qh_data" v-show="show_table">

    <!-- 序号 -->
    <template #i="{ row, index }">
      {{ index }}
    </template>

    <!-- 星星 -->
    <template #stars="{ row, index }">
      <img src="./assets/star.png" v-for="n in qh_data[index].stars">
    </template>

    <!-- 详情按钮 -->
    <template #action="{ row, index }">
      <Button type="primary" size="small" style="margin-right: 5px" @click="show(index)">详情</Button>
    </template>

  </Table>

  <!-- 代码展示/下载 -->
  <div id="code-container" v-show="show_code">
    <Collapse>
      <Panel>
        项目介绍
        <template #content>
          <h2>项目下载：</h2>
          <div><a href="#">github</a></div>
          <div><a href="#">百度网盘</a></div>
          <div><a href="#">数据库下载(下载爬取到的数据文件)</a></div>
          <br>
          <h2>项目流程：数据抓取 -> 前端构建 -> 后端接口开发</h2>
          <br>
          <div>1.数据抓取 -> 技术框架 python,requests,mysql</div>
          <div>2.前端构建 -> 技术框架 vue3,axios,echarts</div>
          <div>3.后端接口开发 -> 技术框架 node.js,express</div>
          <br>
          <h2>项目目录结构：</h2>
          <pre>
.\QHCPS_PROJECT  ->  项目名
│  mysql.txt ->  mysql数据库创建命令
│
├─.vscode
│      settings.json
│
├─spider  ->  爬虫项目目录
│  │  qhcps_spider.py  ->  爬虫文件
│  │
│  └─log  ->  爬虫日志文件
│
└─web  ->  web项目目录
    ├─qhcps_charts -> 前端项目目录
    │  │  .gitignore
    │  │  index.html
    │  │  package-lock.json
    │  │  package.json
    │  │  README.md
    │  │  vite.config.js
    │  │
    │  ├─.vscode
    │  │
    │  ├─node_modules
    │  ├─public
    │  │
    │  └─src
    │      │  App.vue
    │      │  main.js
    │      │
    │      ├─assets
    │      │
    │      └─components
    │
    └─server  ->  后端项目目录
        │  package-lock.json
        │  package.json
        │  server.js  ->  服务器启动文件
        │
        └─node_modules
          </pre>
          
        </template>
      </Panel>
      <Panel>
        项目启动流程
        <template #content>
          <pre>
1.创建数据库(mysql.txt) -> 通过输入 mysql.txt 里的命令创建数据库和表
2.启动爬虫(/spider/qhcps_spider.py) -> (python qhcps_spider.py)直接运行文件即可将网站数据抓取到数据库中，由于没有设置延迟，
  可能会出现服务器拒绝连接导致爬取不到 这里可以通过log文件夹下查看对应的日志信息，在重新从对应的位置开始抓取数据
3.启动服务器(/web/server/server.js) -> (node server.js) 通过 node 启动服务器获得数据接口 http://127.0.0.1:9527
4.启动vue项目(/web/qhcps_charts/) -> (npm run dev) 启动前端项目 http://localhost:5173/
          </pre>
        </template>
      </Panel>
      <Panel>
        核心代码片段(爬虫)
        <template #content>
          <h2 style="color: red;font-weight: bold;">抓取主页数据</h2>
          <h3 style="font-weight: bold;">1.获取主页静态html</h3>
          <img src="../public/s1.png" alt="">
          <h3 style="font-weight: bold;">2.通过 xpath 抓取数据</h3>
          <img src="../public/s2.png" alt="">
          <img src="../public/s3.png" alt="">
          <br>
          <h2 style="color: red;font-weight: bold;">抓取用户时间序列数据</h2>
          <img src="../public/s4.png" alt="">
        </template>
      </Panel>

      <Panel>
        核心代码片段(Vue)
        <template #content>
          <h2 style="color: red;font-weight: bold;">表格组卷</h2>
          <div><img src="../public/v1.png" alt=""></div>
          <h2 style="color: red;font-weight: bold;">表格请求数据</h2>
          <div><img src="../public/v2.png" alt=""></div>
          <div><img src="../public/v3.png" alt=""></div>
          <h2 style="color: red;font-weight: bold;">详情按钮请求数据</h2>
          <div><img src="../public/v4.png" alt=""></div>
        </template>
      </Panel>

      <Panel>
        核心代码片段(后端服务器node)
        <template #content>
          <h2 style="color: red;font-weight: bold;">表格请求数据接口</h2>
          <div><img src="../public/n1.png" alt=""></div>
          <div><img src="../public/n2.png" alt=""></div>
          <h2 style="color: red;font-weight: bold;">详细请求数据接口</h2>
          <div><img src="../public/n3.png" alt=""></div>
          <div><img src="../public/n4.png" alt=""></div>
        </template>
      </Panel>
    </Collapse>
  </div>

  <!-- echarts -->
  <!-- 透明黑色背景 -->
  <div id="dialog_bg" v-show="show_dialog" @click="close_dialog"></div>
  <!-- 图表 div -->
  <div id="dialog" v-show="show_dialog"></div>
</template>

<script>
export default {
  data() {
    return {
      myChart: null,
      show_dialog: false,
      show_table: true,
      show_code: false,
      columns: [
        {
          title: '序号',
          slot: 'i',
          sortable: true
        },
        {
          title: '操盘手',
          key: 'username',
          sortable: true
        },
        {
          title: '最新权益',
          key: 'latest_equity',
          sortable: true
        },
        {
          title: '平均权益',
          key: 'avg_equity',
          sortable: true
        },
        {
          title: '累计净利润',
          key: 'cumulative_net_profit',
          sortable: true
        },
        {
          title: '年净利润率',
          key: 'annual_net_profit_margin',
          sortable: true,
          render: (h, params) => {
            return String(params.row.annual_net_profit_margin) + "%"
          }
        },
        {
          title: '累计手续费',
          key: 'accumulated_handling_fees',
          sortable: true
        },
        {
          title: '年手续费率',
          key: 'annual_handling_fee',
          sortable: true,
          render: (h, params) => {
            return String(params.row.annual_handling_fee) + "%"
          }
        },
        {
          title: '累计净值',
          key: 'cumulative_net_worth',
          sortable: true
        },
        {
          title: '最大回撤率',
          key: 'maximum_retracement_rate',
          sortable: true,
          render: (h, params) => {
            return String(params.row.maximum_retracement_rate) + "%"
          }
        },
        {
          title: '本站评级',
          width: 110,
          slot: 'stars',
          align: 'center',
          sortable: true
        },
        {
          title: '详情',
          slot: 'action',
          align: 'center'
        }
      ],
      qh_data: []
    }
  },
  mounted() {
    // 初始化 echarts
    Object.defineProperty(document.getElementById('dialog'), 'clientWidth', { get: function () { return 1024; } })
    Object.defineProperty(document.getElementById('dialog'), 'clientHeight', { get: function () { return 600; } })
    var dom = document.getElementById('dialog');
    this.myChart = this.$echarts.init(dom)
  },
  created() {
    // 调用 获取表格数据
    this.get_data()
  },
  methods: {
    // 导航栏点击事件
    select_menu: function (name) {
      if (name == 1) {
        this.show_table = true
        this.show_code = false
      } else {
        this.show_table = false
        this.show_code = true
      }

    },
    // 获取表格数据
    get_data: function () {
      this.$axios.get('http://127.0.0.1:9527/get_qh_data')
        .then(response => {
          this.qh_data = response['data']
        })
        .catch(error => {

        })
    },
    // 请求图表数据并展示
    show(index) {

      this.$axios.get('http://127.0.0.1:9527/get_data_by_id?id=' + this.qh_data[index].id).then((res) => {
        this.show_dialog = true

        var option;

        option = {
          title: {
            text: "累计净利润(累计手续费)",
            x: 'center',
            padding: [10, 0, 0, 0]
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            top: '10%',
            containLabel: true
          },
          legend: {
            data: ['累计手续费', '累计净利润'],
            y: 'bottom',
            padding: [0, 0, 20, 0]
          },
          xAxis: {
            type: 'category',
            data: res.data.dtime,
            axisLabel: {
              rotate: "45"
            }
          },
          yAxis: {
            type: 'value',
            max: function () {
              let cnp = Math.max.apply(null, res.data.cumulative_net_profit)
              let ahf = Math.max.apply(null, res.data.accumulated_handling_fees)
              if (cnp > ahf) {
                return cnp
              } else {
                return ahf
              }
            },
            min: function () {
              let cnp = Math.min.apply(null, res.data.cumulative_net_profit)
              let ahf = Math.min.apply(null, res.data.accumulated_handling_fees)
              if (cnp > ahf) {
                return ahf
              } else {
                return cnp
              }
            }
          },
          series: [
            {
              name: '累计手续费',
              data: res.data.accumulated_handling_fees,
              type: 'line',
              smooth: true,
              symbol: 'none',
              lineStyle: {
                normal: {
                  color: 'blue',
                },
              },
              itemStyle: {
                normal: {
                  color: 'blue'
                },
                emphasis: {
                  normal: {
                    color: 'blue'
                  }
                }
              }
            },
            {
              name: '累计净利润',
              data: res.data.cumulative_net_profit,
              type: 'line',
              symbol: 'none',
              lineStyle: {
                normal: {
                  color: 'red',
                },
              },
              itemStyle: {
                normal: {
                  color: 'red'
                },
                emphasis: {
                  normal: {
                    color: 'red'
                  }

                }
              }
            }
          ]
        };

        this.myChart.setOption(option);

      })
    },
    // 关闭对话框
    close_dialog() {
      this.show_dialog = false
    }
  }
}
</script>

<style scss>
body {
  display: inline;
  padding: 0;
  margin: 0;
  border: 0;
  width: 100%;
}


#app {
  display: block;
  width: 100%;
  height: 100%;
}

#dialog_bg {
  position: fixed;
  background-color: black;
  opacity: 0.5;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 999;
}

#dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1024px;
  height: 600px;
  background-color: white;
  opacity: 1;
  z-index: 1000;
  border-radius: 10px;
}</style>
