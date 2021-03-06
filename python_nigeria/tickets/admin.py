from django.contrib import admin

# Register your models here.
from .models import (
    Ticket, TicketPrice, Coupon, TicketSale
)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'ticket_type', 'amount', 'status', 'multiple_tickets', 'quantity']
    list_filter = ['ticket_type__name', 'status']
    search_fields = ['user__email', 'user__username']


@admin.register(TicketPrice)
class TicketPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'current_price', 'early_price_count', 'regular_count', 'total', 'remaining']

    def total(self, obj):
        return obj.purchased_count

    def remaining(self, obj):
        return obj.early_price_count + obj.regular_count - obj.purchased_count

    def get_queryset(self, request):
        query = super(TicketPriceAdmin, self).get_queryset(request)

        return query.with_tickets_purchased()


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['value', 'expired', 'number_of_usage', 'counts']
    actions = 'mark_as_expired'

    def counts(self, obj):
        return obj.usages.count()

    def mark_as_expired(self, request, queryset):
        queryset.update(expired=True)


@admin.register(TicketSale)
class TicketSaleAdmin(admin.ModelAdmin):
    list_display = ['the_ticket_id', 'full_name', 'ticket_type', 'diet', 'tagline', 'ticket']
    list_filter = ['ticket__ticket_type']

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('pk')

    def ticket_type(self, obj):
        return obj.ticket.ticket_type
