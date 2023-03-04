import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import router from './router/index.js'
import { ElMessage } from 'element-plus'
import '../style/styles.css'
import axios from 'axios'

const app = createApp(App)
app.use(ElementPlus, { locale: zhCn })
app.use(router)

axios.defaults.baseURL = 'http://localhost:8080'

axios.interceptors.request.use(config => {
    config.headers.Authorization = window.sessionStorage.getItem("token")
    return config
})

axios.interceptors.response.use(
    response => {
        let data = response.data
        switch (data.code) {
            case 401:
                ElMessage({
                    message: data.message,
                    type: 'error',
                })
                window.sessionStorage.clear()
                router.push("/")
                break;
        }
        return response
    }
)
app.config.globalProperties.$http = axios

app.mount('#app')
