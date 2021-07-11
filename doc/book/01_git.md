
### git基本命令

```shell
# 克隆代码
> git clone https://github.com/defnngj/test_project

# 查看更新
> git status

# 更新将要提交的内容
> git add .
> git add test.py
> git add abc/

# add 撤销
> git reset HEAD
> git reset HEAD test.py

# 提交更新
> git commit -m "update"

# 同步到远程master分支
> git push origin master

# 从远程master分支拉取代码到本地
> git pull origin master

```

### 分支操作

```shell
# 查看全部分支（远程的和本地的）
> git branch -a

# 创建分支
> git branch dev

# 切换分支
> git checkout dev

# 合并分支（把dev分支合并到当前分支）
> git merge dev

```

__分支&冲突合并__

|  main分支   | dev分支  | test分支  |
|  ----  | ----  |----  |
| 分布分支  | A开发分支 | B开发分支  |

main: <--dev <--冲突--test  ok
main: <--test <--冲突--dev

main <<=== dev: <--冲突-- test 
main <<=== test: <--冲突-- dev

test <--冲突-- main
dev <--冲突-- main

### 客户端

github for desktop：
https://desktop.github.com/



### git/github 教程

http://class.itest.info/git
