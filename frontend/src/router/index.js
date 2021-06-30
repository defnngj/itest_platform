import Vue from 'vue'
import VueRouter from 'vue-router'
import Workbench from '../components/home/Workbench.vue'
import Calendar from '../components/scheduling/Calendar.vue'
import FlowLog from '../components/flowlog/FlowLog.vue'
import Project from '../components/project/Project.vue'
import Cases from '../components/case/Cases.vue'
import Reports from '../components/report/Reports.vue'
import Files from '../components/files/Files.vue'
import Monitor from '../components/config/monitor/Monitor.vue'
import Email from '../components/config/email/Email.vue'
import Env from '../components/config/environment/Env.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Workbench',
    component: Workbench
  },
  {
    path: '/scheduling',
    name: 'Calendar',
    component: Calendar
  },
  {
    path: '/flowlog',
    name: 'FlowLog',
    component: FlowLog
  },
  {
    path: '/env',
    name: 'Env',
    component: Env
  },
  {
    path: '/project',
    name: 'Project',
    component: Project
  },
  {
    path: '/cases',
    name: 'Cases',
    component: Cases
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  },
  {
    path: '/files',
    name: 'Files',
    component: Files
  },
  {
    path: '/monitor',
    name: 'Monitor',
    component: Monitor
  },
  {
    path: '/email',
    name: 'Email',
    component: Email
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
