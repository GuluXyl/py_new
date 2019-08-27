from django.urls import include,path
import blog.views

#路由的配置
urlpatterns = [
    #如果URL里面含有hello_world的话就将它转发到blog.views.hello_world这个视图函数里面
    path('hello_world',blog.views.hello_world),
    path('content',blog.views.article_content),
    path('index',blog.views.get_index_page),
    # path('detail', blog.views.get_detail_page),
    path('detail/<int:article_id>', blog.views.get_detail_page)
]