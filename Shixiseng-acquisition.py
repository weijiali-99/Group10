# -*- codeing = utf-8 -*-
# @Time : 2021/11/2 19:40
# @Author : LI Weijia
# @File: BOSS.py
# @Software : PyCharm
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt

def main():
    baseurl="https://resume.shixiseng.com/interns?page="
    datalist=getdata(baseurl)
    savepath=".\\boss.xls"
    savedata(datalist,savepath)

findtitle=re.compile(r'<a.*?>(.*?)</a>')
findlink=re.compile(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')")
findintro=re.compile(r'<span.*title=.*>(.*)</span>')
findlocation=re.compile(r'<span class="city ellipsis" data-v-d5abf57a="">(.*?)</span>')
findproperty=re.compile(r'<span class="ellipsis" data-v-d5abf57a="">(.*?)</span>')
findsalary=re.compile(r'<span class="day font" data-v-d5abf57a="">(.*)/月</span>')
findrequirement=re.compile(r'<span class="font" data-v-d5abf57a="">(.*?)</span>')

def getdata(baseurl):
    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i)+'&type=school&keyword=%E5%95%86%E4%B8%9A%E5%88%86%E6%9E%90'
        html=askURL(url)
        soup=BeautifulSoup(html,"html.parser")

        for item in soup.find_all('div',class_='intern-wrap intern-item'):
            data=[]
            item=str(item)
            title=re.findall(findtitle,item)[0] #岗位名
            data.append(title)
            name=re.findall(findtitle,item)[1] #公司名
            data.append(name)
            link=re.findall(findlink,item)[0] #详情连接
            data.append(link)
            salary = re.findall(findsalary, item)
            if len(salary) != 0:
                data.append(salary[0] + '/月')
            else:
                data.append('薪资面议')
            city=re.findall(findlocation,item) #工作地点
            if len(city)!=0:
                data.append(city[0])
            else:
                data.append(' ')
            requirment = re.findall(findrequirement, item)
            identity = re.findall(findrequirement, item)[0] #学生身份
            if len(identity)!=0:
                data.append(identity)
                xueli=re.findall(findrequirement,item)[1] #学历
                data.append(xueli)
                scale=re.findall(findrequirement,item)[2] #公司规模
                data.append(scale)
            else:
                data.append(' ')
                data.append(' ')
                data.append(' ')

            introduction = re.findall(findintro, item)[0]  # 公司介绍
            if len(introduction) != 0:
                data.append(introduction)
            else:
                data.append(' ')
            # prop=re.findall(findproperty,item)
            # data.append(prop)
            datalist.append(data)
    return datalist

def savedata(datalist,savepath):
    # pass
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('实习僧岗位',cell_overwrite_ok=True)
    col = ('岗位名称', '公司名', '招聘详情页', '薪资', '工作地点', '身份要求', '学历要求', '公司规模','公司简介')
    for i in range(0,9):
        sheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,9):
            sheet.write(i+1,j,data[j])
    book.save('business_analysis.xls')

def askURL(url):
    head={
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 95.0.4638.54 Safar/ 537.36"
    }
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html



if __name__=="__main__":
    main()















































