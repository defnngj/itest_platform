# frontend

前端模板

## Project setup

* 安装依赖项目依赖，根据`package.json`文件

```shell
npm install
```

* 编译和热加载

```shell
npm run serve  # 开发环境（使用mock api）
npm run local-serve  # 本地联调环境(调用本地开发的 api)
npm run prod-serve  # 产线环境(使用域名 api)
```

* 编译和打包项目

```shell
npm run build  # 开发环境
npm run local-build   # 本地联调环境
npm run prod-build  # 产线环境(用这个打包)
```

* 运行e2e测试

```shell
npm run test:e2e
```

* Lints and fixes files

```shell
npm run lint
```

* Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).shell

## 开发规范

* 文件命名

> html 小写字母+横线，例如:index.html，org-list.html
> js 小写字母+横线，例如:i18n.js，en-US.js
> vue 驼峰命名，首字母大写，例如Login.vue，HeaderUser.vue

* 变量命名

> 常量 大写字母加下划线，例如`:const ROLE_ADMIN='admin'`
> 变量 驼峰命名，首字母小写，例如`let name`，`let currentProject`
> 方法 驼峰命名，首字母小写，例如`open(){}`，`openDialog()`

* Vue组件

> 导出名称 驼峰命名，首字母大写，例如`MsUser`

* 样式规范

> 均写入vue文件的`<style scope></style>`标签内，非全局样式必须添加`scope`
> 修改ElementUI的样式，仅在必要情况下写在`<style></style>`
> 命名 小写字母+横线，例如`.menu`，`.header-menu`，`#header-top`

* 格式要求

> 遵循.editorconfig

* Vue风格指南
https://cn.vuejs.org/v2/style-guide/
