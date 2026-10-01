from django.contrib import admin

from .models import Establishment, Membership


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    autocomplete_fields = ["user"]


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "establishment", "role", "status")
    list_filter = ("role", "status", "establishment")
    search_fields = ("user__email", "user__name", "establishment__name")
    autocomplete_fields = ["user"]