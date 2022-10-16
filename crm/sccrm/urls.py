
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from musicians.views import LandingPageView, SignupView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('musicians/', include('musicians.urls', namespace="bands")),
    path('bands/', include('bands.urls', namespace="musicians")),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset-password-done/', PasswordResetView.as_view(), name='reset-password-done'),
    path('reset-password/', PasswordResetDoneView.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name='reset-password-complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)