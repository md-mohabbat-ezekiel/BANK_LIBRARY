from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path("books/<slug:book_slug>", Home.as_view(), name="book_slug"),
    path('customers/', include("customers.urls")),
    path("books/", include("books.urls")),
    path("transactions/", include("transactions.urls"))

]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
