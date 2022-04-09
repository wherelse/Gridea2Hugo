---
title: gridea to hugo 转换脚本
date: 2022-04-09
slug: gridea-to-hugo-convert-script
---
为了方便的迁移Gridea的md文章至Hugo，我写了一个转换脚本，可以批量将Gridea的文件头FrontMatter转换到Hugo的文件头，同时还支持对md文件内的图片链接进行转换。

## Gridea与Hugo差异
Gridea的md文件默认都存储在配置文件夹的`posts`文件夹中，图片则默认存储在`post-images`文件夹中。

Hugo的md文件默认都存储在配置文件夹的`content/post`文件夹中，图片则一般默认存储在`static`文件夹中。

在迁移Gridea的md文件至Hugo时，需要将Gridea的md文件头FrontMatter转换到Hugo的文件头，同时还要对md文件内的图片链接进行转换。
## 脚本使用
首先设置脚本中的文件夹路径，`readpath`为Gridea的md文件夹路径，`writepath`为转换后输出的符合Hugo规则的md文件夹路径，`imgurl`为Hugo的md文件图片相对存储路径，`FeatureImgurl`为Hugo的md文件封面图片相对存储路径。

若不需要对图片链接进行转换，可以将`imgurl`和`FeatureImgurl`设置为空。

具体设置可以参考以下内容：
```python
readpath = './posts' # 需要转换的文件夹
writepath = './post' # 输出文件夹
imgurl = '../../static/post-images/' # 图片路径
FeatureImgurl = '/post-images/'  # 封面图片路径
```

建议将Gridea的`post-images`完整的复制到Hugo的`static`文件夹中，并按照以上内容设置脚本文件内容这要转换后不需要对图片做特殊的处理。

然后将脚本文件复制到Gridea的配置文件夹中，并运行脚本即可，就可得到转换完成的md文件，md文件会统一输出到`writepath`对于的文件夹中。
## 文件头FrontMatter的处理
1. 文件名，Gridea的文件名和文章的链接一致，所以直接转化的话，无法方便的看出文章的内容，文件名重命名为文章的标题`title`。
2. 文章的url，由于文件名更改为标题，所以将文件的url信息转换至`slug`中。
3. 其他有效信息对应转换，如`date`、`tags`等，无效的信息就选择丢弃。

## 使用注意
1. 因为需要将标题转换至文件名，所以文件名中不能包含特殊字符，如`.`、`:`等，否则会导致脚本出错。

## Hugo goldmark 配置
在Gridea中，md文件在一行的结尾插入一个回车就会默认换行，而在Hugo中，默认情况下并不会换行，而是需要插入两个空格才会换行，但是可以通过goldmark配置文件进行修改，在`config.toml`中的`[markup]`中的`[markup.goldmark.renderer]`选项中添加如下内容：
```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      hardWraps = true #是否使用回车换行
```
## Hugo Latex公式渲染问题解决方案
Hugo 默认使用的goldmark渲染器在渲染latex公式时，会错误的处理`_`和`\\`，导致文章中的latex公式渲染出错，官方现在给出的解决方案主要是使用`{{<math>}}`shortcode包裹latex，或者使用`\\\\`来代替`\\`，这两个解决方案都不完美，都无法兼容其他的markdown编辑器。

下面仓库中提供了一个编译hugo文件方式实现的解决方案，通过导入goldmark-mathjax，有效的解决了上述问题，但是官方并没有将此方法合并到主分支中，所以只能下载经过修改的编译版本。
[https://github.com/xjzsq/hugo](https://github.com/xjzsq/hugo)

