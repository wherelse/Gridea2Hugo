import os
import re

readpath = './posts' # 需要转换的文件夹
writepath = './post' # 输出文件夹
imgurl = '../../static/post-images/' # 图片路径
FeatureImgurl = '/post-images/'  # 封面图片路径

if __name__ == '__main__':
    # 获取文件夹下所有文件名
    mdfilesnames = []
    rootdir = os.path.join(readpath)
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith(".md"):
                mdfilesnames.append(dirpath+'/'+filename)
    # print(mdfilesnames)
    if not os.path.exists(writepath):#如果输出文件夹不存在，则创建
        os.makedirs(writepath)

    for file in mdfilesnames:
        with open(file,'r',encoding='utf-8') as f:
            content = f.read()
            # 替换md文件头内容
            FrontMatter = re.search(r'---\n(.*?)\n---', content, re.S).group(1) # 匹配文件头内容
            FrontMatter = FrontMatter.split('\n')# 将文件头内容按行分割
            title = FrontMatter[0].split(':')[1].strip() #获取文章标题
            date = ''.join( FrontMatter[1].split('date:')[1].split(' ')[1] )# 获取文章日期
            tags = FrontMatter[2].split(':')[1].strip() # 获取文章标签
            mdurl = file.split('/')[-1].split('.')[0] # 获取文章url slug
            feature = FrontMatter[5].split(':')[1].split('/')[-1] # 获取文章封面图片
            if feature != ' ' and FeatureImgurl != '':
                feature = FeatureImgurl + feature
            FrontMatterHugo = '---\n' \
                'title: '+title+'\n' \
                'date: '+date+'\n' \
                'tags: '+tags+'\n' \
                'slug: '+mdurl+'\n' \
                'featuredImage: '+feature+'\n' \
                '---\n'
            repattern = re.compile(r'---\n(.*?)\n---', re.S)
            content = re.sub(repattern, FrontMatterHugo, content)
            #替换<!--more-->标签
            content = content.replace('<!-- more -->', '<!--more-->')
            #替换图片路径
            if imgurl != '':
                repattern = re.compile(r'!\[.*\]\((.*)\)')
                newurl = []
                result = re.findall(repattern, content)
                for url in result:
                    newurl.append(imgurl+url.split('/')[-1])
                content = re.sub(repattern, lambda x: '![](' + newurl[result.index(x.group(1))]+')', content)
            #写入修改后的文件
            title = title.strip('\'')
            title = title.replace('/','')
            with open(writepath+'/'+title+'.md','w',encoding='utf-8') as f:
                f.write(content)
