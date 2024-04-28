from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path("", views.loginPage, name="Login"),
    path("logout/", views.logoutUser, name="Logout"),
    path("signup/", views.signup, name="Signup"),
    path("home/", views.index, name="StoreHome"),
    path("about/", views.about, name="AboutUs"),
    path("addmedicine/", views.addmedicine, name="AddMedicine"),
    path("inventory/", views.inventory, name="Inventory"),
    path("sellmedicine/<int:Medicine_ID>/", views.sellmedicine, name="SellMedicine"),
    path("records/", views.records, name="Records"),
    path("delete/<int:Medicine_ID>/", views.delete_med, name="DeleteMed"),
    path("delete_rec/<int:Purchase_ID>/", views.delete_rec, name="DeleteRec"),
    path("<int:Medicine_ID>/", views.update_med, name="UpdateMed"),
    path('accounts/', include('django.contrib.auth.urls')),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="store/password_reset_form.html"), name="password_reset_form"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_complete.html"), name="password_reset_complete"),

]
