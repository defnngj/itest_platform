/**
* @module utils
* @author huzhiheng
* @date 2021年02月01日
* @desc calendar-heatmap 插件扩展
*/

// 修复calendar-heatmap插件样式问题
export function fixCalendarHeatmapStyle() {
  document.querySelectorAll('svg#heatmap > g > text')[0].setAttribute('x', '16')
  document.querySelectorAll('svg#heatmap > g > text')[1].setAttribute('x', '66')
  document.querySelectorAll('svg#heatmap > g > text')[2].setAttribute('x', '116')
  document.querySelectorAll('svg#heatmap > g > text')[3].setAttribute('x', '166')
  document.querySelectorAll('svg#heatmap > g > text')[4].setAttribute('x', '216')
  document.querySelectorAll('svg#heatmap > g > text')[5].setAttribute('x', '266')
  document.querySelectorAll('svg#heatmap > g > text')[6].setAttribute('x', '316')
  document.querySelectorAll('svg#heatmap > g > text')[7].setAttribute('x', '366')
  document.querySelectorAll('svg#heatmap > g > text')[8].setAttribute('x', '416')
  document.querySelectorAll('svg#heatmap > g > text')[9].setAttribute('x', '466')
  document.querySelectorAll('svg#heatmap > g > text')[10].setAttribute('x', '516')
  document.querySelectorAll('svg#heatmap > g > text')[11].setAttribute('x', '566')
}
