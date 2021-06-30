import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import './assets/theme/index.css'
import VueHighlightJS from 'vue-highlightjs'
import 'highlight.js/styles/color-brewer.css'
import 'github-markdown-css/github-markdown.css'
import isNewVersion from '/src/libs/versionUpdate'

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.use(VueHighlightJS)

router.beforeEach(async (to, from, next) => {
  // 判断当前代码版本是否与服务器中代码版本一致，如不一致则刷新页面获取最新
  await isNewVersion()
  next()
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
