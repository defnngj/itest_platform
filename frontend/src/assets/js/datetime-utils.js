/**
* @module utils
* @author huzhiheng
* @date 2021年1月12日
* @desc 日期时间的格式转换
*/

// 时间戳转字符串
// 入参：1610501400000
// 返回值：2021-1-13 9:30:00
export function timestampToString(timestamp) {
  const date = new Date(timestamp)
  const y = date.getFullYear()
  let m = date.getMonth() + 1
  m = m < 10 ? ('0' + m) : m
  let d = date.getDate()
  d = d < 10 ? ('0' + d) : d
  let h = date.getHours()
  h = h < 10 ? ('0' + h) : h
  let minute = date.getMinutes()
  minute = minute < 10 ? ('0' + minute) : minute
  let second = date.getSeconds()
  second = second < 10 ? ('0' + second) : second
  return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second
}

// 字符串转时间戳
// 入参： 2021-1-13 9:30:00
// 返回值：1610501400000
export function stringToTimestamp(str) {
  const dateFormat = new Date(Date.parse(str.replace(/-/g, '/')))
  const timestamp = dateFormat.getTime()
  return timestamp
}

export function getNowTime() {
  const date = new Date()
  const now_time = timestampToString(date.getTime()).slice(11, 19)
  return now_time
}
