import './assets/main.css'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import axios from 'axios'
import * as echarts from 'echarts';


import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import App from './App.vue'

const app = createApp(App)

app.config.globalProperties.$axios = axios
app.config.globalProperties.$echarts = echarts;
app.use(ViewUIPlus)
app.mount('#app')
