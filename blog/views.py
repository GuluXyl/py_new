from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
from django.core.paginator import Paginator

# Create your views here.


def hello_world(resquest):
    return HttpResponse("hello world")

def article_content(request):
    article = Article.objects.all()[0]
    title=article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    pubish_date = article.publish_date
    return_str = 'title:%s,brief_content:%s,' \
                 'content:%s,article_id:%s,pubish_date:%s'%(title,brief_content,
                                                                content,article_id,
                                                                pubish_date)
    return HttpResponse(return_str)

def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ',page)
    all_article = Article.objects.all()
    # 由于正序展示的是最远发布的文章,加个负号表示最近的
    top5_article_list = Article.objects.order_by('-publish_date')[:5]
    paginator = Paginator(all_article,6)
    page_num = paginator.num_pages
    print('page num:',page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    # render()的意思就是把模板系统跟数据(这里指all_article)进行渲染然后返回
    # render()里面接收参数request,首页的模板(blog/index.html),渲染页面所需要的数据,用字典包起来

    return render(request,'blog/index.html',
                  {
                     'article_list':page_article_list,
                      'page_num':range(1,page_num + 1),
                      'curr_page':page,
                      'next_page':next_page,
                      'previous_page':previous_page,
                      'top5_article_list':top5_article_list
                })

def get_detail_page(request,article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    for index,article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break
    section_list = curr_article.content.split('\n')
    return render(request,'blog/detail.html',
                  {
                      'curr_article': curr_article,
                      'section_list': section_list,
                      'previous_article':previous_article,
                      'next_article':next_article
                  })
