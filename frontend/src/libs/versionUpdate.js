// 获取当前版本号--时间戳
import axios from 'axios'
import Vue from 'vue'

const isNewVersion = function() {
  return new Promise(function(resolve) {
    if (process.env.NODE_ENV !== 'production') {
      resolve(false)
    } else {
      axios.get('/version.json').then(res => {
        const version = res.data
        const localVersion = JSON.parse(localStorage.getItem('version'))
        const isUpdated = localVersion !== null && localVersion.version === version.version
        if (!isUpdated) {
          Vue.prototype.$message({
            type: 'info',
            message: 'Updating'
          });
          version.needNotification = true
          localStorage.setItem('version', JSON.stringify(version))
          window.location.reload()
        } else {
          resolve(false)
        }
      })
    }
  })
};

export default isNewVersion
