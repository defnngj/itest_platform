<!--
/**
* @module components
* @author huzhiheng
* @date 2020年12月15日
* @desc 页面导航组件
*/
-->
<template>
  <div class="navigation">
    <el-container>
      <el-container>
        <el-aside width="160px" style="background-color: #313a46">
          <el-menu text-color="#838f9c" active-text-color="#12263f" :default-active="onRoutes">
            <div class="redirect-logo">
              <img src="../assets/logo.png" class="img-logo" />
            </div>
            <router-link to="/">
              <el-menu-item index="1" class="menu-option">
                <i class="el-icon-s-home"></i>
                <template #title> 首页</template>
              </el-menu-item>
            </router-link>
            <router-link to="/scheduling">
              <el-menu-item index="2" class="menu-option">
                <i class="el-icon-date"></i>
                <template #title>日程安排</template>
              </el-menu-item>
            </router-link>
            <router-link to="/flowlog">
              <el-menu-item index="3" class="menu-option">
                <i class="el-icon-s-marketing"></i>
                <template #title>流量日志</template>
              </el-menu-item>
            </router-link>
            <router-link to="/project">
              <el-menu-item index="4" class="menu-option">
                <i class="el-icon-menu"></i>
                <template #title>项目管理</template>
              </el-menu-item>
            </router-link>
            <router-link to="/cases">
              <el-menu-item index="5" class="menu-option">
                <i class="el-icon-s-grid"></i>
                <template #title>用例管理</template>
              </el-menu-item>
            </router-link>
            <router-link to="/reports">
              <el-menu-item index="6" class="menu-option">
                <i class="el-icon-document"></i>
                <template #title>报告管理</template>
              </el-menu-item>
            </router-link>
            <router-link to="/files">
              <el-menu-item index="7" class="menu-option">
                <i class="el-icon-folder"></i>
                <template #title>文件管理</template>
              </el-menu-item>
            </router-link>
            <el-submenu index="8" class="menu-option">
              <template #title><i class="el-icon-setting"></i>配置管理</template>
              <el-menu-item-group class="menu-option">
                <router-link to="/monitor">
                  <el-menu-item index="8-1">监控分组</el-menu-item>
                </router-link>
              </el-menu-item-group>
              <el-menu-item-group class="menu-option">
                <router-link to="/email">
                  <el-menu-item index="8-2">邮件分组</el-menu-item>
                </router-link>
              </el-menu-item-group>
              <el-menu-item-group class="menu-option">
                <router-link to="/env">
                  <el-menu-item index="8-3">环境管理</el-menu-item>
                </router-link>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-container>
          <el-header style="text-align: right; font-size: 12px">
            <el-dropdown @command="handleCommand" trigger="click" style="margin-top: 10px;">
              <el-avatar size="small" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
              <el-dropdown-menu slot="dropdown" style="width: 120px">
                <el-dropdown-item command="itest">
                  <i class="el-icon-s-platform"></i>重定向
                </el-dropdown-item>
                <el-dropdown-item command="logout">
                  <i class="el-icon-switch-button"></i>退出
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-header>
          <el-main>
            <router-view> </router-view>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
    <!-- 更新通知 -->
    <div class="notification" v-if="showReleaseListDialog">
      <notificationDialog @cancel="cancelNotification"></notificationDialog>
    </div>
  </div>
</template>


<script>
import notificationDialog from '../components/notification/NotificationDialog.vue'

export default {
  name: 'navigation',
  components: { notificationDialog },
  computed: {
    onRoutes() {
      if (this.$route.path === '/scheduling') {
        return '2'
      } else if (this.$route.path === '/flowlog') {
        return '3'
      } else if (this.$route.path === '/project') {
        return '4'
      } else if (this.$route.path === '/cases') {
        return '5'
      } else if (this.$route.path === '/reports') {
        return '6'
      } else if (this.$route.path === '/files') {
        return '7'
      } else if (this.$route.path === '/monitor') {
        return '8-1'
      } else if (this.$route.path === '/email') {
        return '8-2'
      } else if (this.$route.path === '/env') {
        return '8-3'
      }
      return '1'
    }
  },
  data() {
    return {
      showReleaseListDialog: false
    }
  },
  mounted() {
    this.showNotification()
  },

  methods: {
    // 退出登录
    handleCommand(command) {
      switch (command) {
        case 'logout':
          document.getElementsByClassName('sign-out-btn')[0].click();
          break;
        case 'itest':
          window.open('http://www.itest.info/', '_blank')
          break;
        default:
          break;
      }
    },
    showNotification() {
      const localVersion = JSON.parse(localStorage.getItem('version'))
      this.showReleaseListDialog = localVersion !== null && localVersion.needNotification === true
    },
    cancelNotification() {
      const localVersion = JSON.parse(localStorage.getItem('version'))
      localVersion.needNotification = false
      localStorage.setItem('version', JSON.stringify(localVersion))
      this.showReleaseListDialog = false
    }
  }
}
</script>

<style>
.navigation {
  height: 100%;
}

.el-container {
  height: 100%;
}

.redirect-logo {
  background-color: #313a46;
  line-height: 60px;
  padding-bottom: 0px;
  width: 160px;
}

.img-logo {
  display: inline-block;
  vertical-align: middle;
  height: 22px;
}

.el-header {
  background-color: #fff;
  color: #313a46;
  line-height: 60px;
  text-align: center;
}

.el-aside {
  background-color: #fff;
  color: #333;
  text-align: center;
  line-height: 160px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

a {
  color: #838f9c;
  text-decoration: none;
}

.menu-option {
  text-align: left;
  background-color: #313a46;
  color: #fff;
  width: 160px;
}
.el-menu-item-group__title {
  padding: 0 !important;
}
.el-menu-item.is-active {
  color: #fff !important;
  background-color: #313a46 !important;
}
.span-breadcrumb {
  float: right;
  margin-top: 10px;
}

.el-breadcrumb__inner a, .el-breadcrumb__inner.is-link {
  color: #727cf5 !important;
}

</style>
