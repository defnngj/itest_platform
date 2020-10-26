# git的使用

* 克隆项目

```shell
git clone https://github.com/defnngj/test_dev3
```

* 查看状态

```shell
git status
```

* 提交给git管理

```shell
git add helle.py
```

* 版本提交

```shell
git commit -m "hello py"
```

* 提高到远程仓库

```shell
git push origin master
```

## 分支来管理项目

* master
* dev
* zhiheng
* ...

* 查看当前分支

```shell
git branch -l
```

* 创建分支

> git branch dev

切换分支：
git checkout dev

合并分支（把dev合并到master）：
git merge dev

# 代码的冲突

public.py

> A. 改了
> B. 改了
> B. 提交
> A. 提交 --> 问题：冲突，合并冲突，再去解决冲突。

站在A的角度：

* 有冲突

```shell
git pull origin dev
From https://github.com/defnngj/test_dev3
 * branch            dev        -> FETCH_HEAD
Auto-merging helle.py
CONFLICT (content): Merge conflict in helle.py
Automatic merge failed; fix conflicts and then commit the result.
```

* 提交冲突的文件

```shell
git add helle.py
git commit -m "A dev change"
```

* 解决冲突

```shell
vim helle.py

git add helle.py
git commit -m "A and B 解决冲突"
```
