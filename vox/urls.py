# url - view - template
from django.urls import path, reverse_lazy
from .views import Homepage, Homevozes, Detalhesvoz, Pesquisa, Editarperfil, Editardublador, Homevozes3
from django.contrib.auth import views as auth_view


app_name = 'vox'

urlpatterns = [

    path('', Homepage.as_view(), name="homepage"),
    path('vozes/', Homevozes.as_view(), name="homevozes"),
    path('vozes3/', Homevozes3.as_view(), name="homevozes3"),
    path('vozes/<int:pk>', Detalhesvoz.as_view(), name="detalhesvoz"),
    path('pesquisa/', Pesquisa.as_view(), name='pesquisa'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('editarperfil/<int:pk>', Editarperfil.as_view(), name="editarperfil"),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html',
                                                             success_url=reverse_lazy('vox:homevozes')), name='mudarsenha'),
    path('admin/vox/dubladore/<int:pk>', Editardublador.as_view(), name="editorialised"),

]